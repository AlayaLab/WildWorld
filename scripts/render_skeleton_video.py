import argparse
import ast
import csv
import json
import os
import subprocess

import cv2  # type: ignore[import-untyped]
import numpy as np
import tqdm  # type: ignore[import-untyped]
from scipy.spatial.transform import Rotation

W, H, FPS = 1280, 720, 30.0
NEAR = 0.05  # near-plane (world units) for clipping bones that cross z=0

# npz key "<kind><slot>_<skel_id>" -> skeleton_edges.json key
EDGE_KEY = {"m": "em_{skel_id}", "n": "npc", "w": "wp_{skel_id}"}
# BGR draw colors + line thickness per kind (all white, thickness 2)
STYLE = {"m": ((255, 255, 255), 2), "n": ((255, 255, 255), 2), "w": ((255, 255, 255), 2)}


def load_camera(state_csv: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """state.csv -> (K (N,4) fx fy cx cy, pos (N,3), quat_xyzw (N,4)).

    Invalid-camera frames are all-nan tuples in the csv; ast.literal_eval
    parses `nan` fine, so they surface as NaN rows here.
    """
    Ks, poss, quats = [], [], []
    with open(state_csv) as f:
        for row in csv.DictReader(f):
            Ks.append(ast.literal_eval(row["camera.K"]))
            poss.append(ast.literal_eval(row["camera.pos"]))
            quats.append(ast.literal_eval(row["camera.rot"]))
    return np.array(Ks), np.array(poss), np.array(quats)


def edges_for(npz_key: str, edge_table: dict[str, list[list[int]]]) -> np.ndarray:
    kind, skel_id = npz_key[0], npz_key.split("_", 1)[1]
    return np.array(edge_table[EDGE_KEY[kind].format(skel_id=skel_id)], dtype=int)


def to_cv_cam(joints_w: np.ndarray, pos: np.ndarray, quat: np.ndarray) -> np.ndarray:
    """(N, J, 3) world -> OpenCV camera frame (X-right, Y-down, Z-forward).

    p_gl = R^T (X - t) done batched as (X - t) @ R; GL->CV flips y and z.
    """
    R = Rotation.from_quat(quat).as_matrix()  # (N, 3, 3) c2w, GL camera frame
    p = np.einsum("njk,nkl->njl", joints_w - pos[:, None, :], R)
    return p * np.array([1.0, -1.0, -1.0])


def draw_entity(img: np.ndarray, p_cv: np.ndarray, K4: np.ndarray, edges: np.ndarray, kind: str) -> None:
    """Draw one entity's bones for one frame. p_cv: (J, 3) OpenCV cam coords."""
    color, thickness = STYLE[kind]
    fx, fy, cx, cy = K4

    a, b = p_cv[edges[:, 0]], p_cv[edges[:, 1]]  # (E, 3) bone endpoints
    ok = ~(np.isnan(a).any(axis=1) | np.isnan(b).any(axis=1))
    # Clip bones crossing the near plane: keep those with at least one endpoint
    # in front, and move the behind endpoint to the z=NEAR intersection.
    front = (a[:, 2] > NEAR) | (b[:, 2] > NEAR)
    for i in np.nonzero(ok & front)[0]:
        pa, pb = a[i].copy(), b[i].copy()
        if pa[2] <= NEAR:
            pa += (pb - pa) * (NEAR - pa[2]) / (pb[2] - pa[2])
        elif pb[2] <= NEAR:
            pb += (pa - pb) * (NEAR - pb[2]) / (pa[2] - pb[2])
        ua = (int(round(fx * pa[0] / pa[2] + cx)), int(round(fy * pa[1] / pa[2] + cy)))
        ub = (int(round(fx * pb[0] / pb[2] + cx)), int(round(fy * pb[1] / pb[2] + cy)))
        cv2.line(img, ua, ub, color, thickness, cv2.LINE_AA)


def start_ffmpeg(output: str, fps: float) -> subprocess.Popen:
    return subprocess.Popen(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "bgr24",
            "-s",
            f"{W}x{H}",
            "-r",
            f"{fps}",
            "-i",
            "-",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            output,
        ],
        stdin=subprocess.PIPE,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("sample_dir", help="sample directory holding state.csv + skeleton.npz")
    parser.add_argument("--edges", help="skeleton_edges.json path")
    parser.add_argument("-o", "--output", default=None, help="output mp4 (default ./<sample>_skeleton.mp4)")
    parser.add_argument("--overlay-rgb", action="store_true", help="draw over the sample's rgb.mp4 frames")
    parser.add_argument("--max-frames", type=int, default=None, help="render only the first N frames")
    parser.add_argument("--fps", type=float, default=FPS)
    args = parser.parse_args()

    sample_dir = args.sample_dir.rstrip("/")
    output = args.output or f"{os.path.basename(sample_dir)}_skeleton.mp4"
    assert not os.path.realpath(output).startswith(os.path.realpath("data") + os.sep), "refusing to write into data/"

    with open(args.edges) as f:
        edge_table = json.load(f)

    K, cam_pos, cam_quat = load_camera(os.path.join(sample_dir, "state.csv"))
    N = len(K)
    cam_ok = ~np.isnan(cam_quat).any(axis=1)
    # Rotation.from_quat rejects NaN rows — substitute identity, masked at draw time.
    cam_quat = np.where(cam_ok[:, None], cam_quat, [0.0, 0.0, 0.0, 1.0])

    # Project every entity for all frames up front (vectorized); draw per frame.
    entities: list[tuple[str, np.ndarray, np.ndarray]] = []  # (kind, p_cv (N,J,3), edges)
    with np.load(os.path.join(sample_dir, "skeleton.npz")) as z:
        for key in sorted(z.files):
            assert z[key].shape[0] == N, f"{key}: {z[key].shape[0]} frames != state.csv {N} rows"
            entities.append((key[0], to_cv_cam(z[key], cam_pos, cam_quat), edges_for(key, edge_table)))

    num_frames = min(N, args.max_frames) if args.max_frames else N
    cap = cv2.VideoCapture(os.path.join(sample_dir, "rgb.mp4")) if args.overlay_rgb else None

    encoder = start_ffmpeg(output, args.fps)
    assert encoder.stdin is not None
    for i in tqdm.tqdm(range(num_frames), mininterval=1):
        if cap is not None:
            ret, img = cap.read()
            assert ret, f"rgb.mp4 ended early at frame {i}"
        else:
            img = np.zeros((H, W, 3), dtype=np.uint8)
        if cam_ok[i]:
            for kind, p_cv, edges in entities:
                draw_entity(img, p_cv[i], K[i], edges, kind)
        encoder.stdin.write(img.tobytes())

    encoder.stdin.close()
    assert encoder.wait() == 0, "ffmpeg failed"
    if cap is not None:
        cap.release()
    print(f"Wrote {num_frames} frames to {output}")
