import os
import tempfile

import numpy as np
from PIL import Image

import predyct


def main():
    with tempfile.TemporaryDirectory() as tmp_dir:
        img_path = os.path.join(tmp_dir, "0.png")
        Image.new("RGB", (2, 2), (0, 0, 0)).save(img_path)
        labels_path = os.path.join(tmp_dir, "test_labels.npy")
        np.save(labels_path, np.array([1, 2, 3]))

        images = predyct.list_image_files(tmp_dir)
        assert images == ["0.png"]

        masked_paths = predyct.mask_labels_in_dir(tmp_dir)
        assert len(masked_paths) == 1
        masked = np.load(masked_paths[0])
        assert np.isnan(masked).all()

    print("OK")


if __name__ == "__main__":
    main()
