# Data

This directory documents how the project data are organized. The assigned field-image recordings may be held in the course-designated storage location rather than committed to Git.

## Data handling

- Follow the instructor's rules for access, sharing, and storage.
- Do not upload restricted source images, annotation files, or derived data to this repository unless the course explicitly permits it.
- Keep original recordings unchanged.
- Use stable image IDs and record the source recording/path in the manifest.
- Record missing metadata as unknown rather than guessing.
- If images are cropped into tiles, preserve the parent image ID and crop coordinates.
- Keep image files and their masks paired by a consistent identifier.

## Expected dataset artifacts

The final location and naming convention should be agreed by the team and recorded here when known.

- **Image manifest:** image ID, source recording, dimensions, relevant metadata, quality notes, and selection status.
- **Images:** selected source images or tiles in the approved storage location.
- **Masks:** lossless, single-channel PNG files with class IDs 0 (background), 1 (sugar beet), 2 (weed), and 255 (ignore).
- **Native annotation export:** project/export from the selected annotation tool, stored in an approved location.
- **Validation report:** image-mask correspondence, dimensions, allowed class IDs, and summary statistics.

Do not add example or placeholder records to the real manifest without clearly marking them as examples. Only record verified observations as dataset facts.
