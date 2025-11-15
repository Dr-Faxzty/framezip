import os
import shutil
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress

def get_mse(img1: np.ndarray, img2: np.ndarray):
    """
    Calculate the Mean Squared Error (MSE) between two images.
    
    Args:
        img1 (numpy.ndarray): First image.
        img2 (numpy.ndarray): Second image.
    """
    err = np.sum((img1.astype("float32") - img2.astype("float32")) ** 2)
    err /= float(img1.shape[0] * img1.shape[1] * img1.shape[2])
    return err

def compute_mse_pair(args):
    """
    Compute MSE value for a single pair of frames.
    
    Args:
        args (tuple): (row_index, col_index, frame_i, frame_j)
    
    Returns:
        tuple: (row_index, col_index, mse_value)
    """
    i, j, frame_i, frame_j = args
    mse = get_mse(frame_i, frame_j)
    return i, j, mse

def sort_frames(frames: list, mse_path: str) -> list:
    """
    Sort frames based on visual similarity using MSE.
    
    Args:
        frames (list): List of image file paths.
        
    Returns:
        list: Sorted list of image file paths.
    """
    print("\nCompression reordering:")
    MSES = [[0] * len(frames) for _ in range(len(frames))]
    
    if os.path.exists(mse_path):
        print("\n[ℹ️] Loading existing MSE matrix from 'mses.csv'...")
        MSES = np.loadtxt(mse_path, delimiter=",").tolist()
    else:
        num_frames = len(frames)
        tasks = []
        for i in range(num_frames):
            for j in range(i + 1, num_frames):
                tasks.append((i, j, frames[i], frames[j]))
        
        with Progress() as p:
            task = p.add_task("[red]Calculating MSE matrix...", total=len(tasks))
            
            with ThreadPoolExecutor() as executor:
                futures = {executor.submit(compute_mse_pair, args): args for args in tasks}
                
                for future in as_completed(futures):
                    i, j, mse_value = future.result()
                    
                    MSES[i][j] = mse_value
                    MSES[j][i] = mse_value
                    p.update(task, advance=1)

        print("\n[✅] MSE matrix calculation completed, saving to 'mses.csv'...")
        np.savetxt(mse_path, MSES, delimiter=",")

    print("\nMSE Sorting:")
    
    reordered_frames = []
    frames_idxs = []
    first = 0
    maxi = sum(MSES[0])
    for i in range(1, len(frames)):
        tmp = sum(MSES[i])
        if maxi < tmp:
            maxi = tmp
            first = i
    
    reordered_frames.append(frames[first])
    frames_idxs.append(first)
    
    for _count in range(len(frames) - 1):
        prv_frame = frames_idxs[-1]
        next_frame = 0
        mini = float('inf')
        for j in range(len(frames)):
            if j in frames_idxs:
                continue
            if mini > MSES[prv_frame][j]:
                mini = MSES[prv_frame][j]
                next_frame = j
        reordered_frames.append(frames[next_frame])
        frames_idxs.append(next_frame)

    return reordered_frames, frames_idxs