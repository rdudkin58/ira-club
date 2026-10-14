# Automatic image publication

Telegram image tasks are completed by the existing GPT Telegram Bridge. The
assistant generates and visually checks images, then uploads binary PNG files
through the authenticated GitHub connector. The user does not upload archives.

1. Read current main and related PRs. Generate/edit using imagegen, inspect every
   final image for ghost text, cropping, duplicate headlines and spelling.
2. Normalize deliverable dimensions (Stories: 1080 × 1920), check actual PNG
   bytes, dimensions, file size and calculate Git blob SHA and SHA-256 locally.
3. Read `scripts/upload_image_blobs.js` and run it inside `functions.exec`.
   Set `image_upload_inputs` using `store`: repository `rdudkin58/ira-club`,
   absolute path to `scripts/binary_chunk.py`, and a `files` list containing
   `local_path`, repository `path`, and expected `git_blob_sha` for each file.
   The helper returns bounded base64 chunks; keep them inside code mode, never
   print base64 to the conversation. GitHub create_blob uses encoding=base64.
4. Create a tree from the latest base tree with `image_upload_tree_elements`,
   HTML references and a publication manifest. Create one commit on a feature
   branch, open a PR, verify its diff and checks, then merge within the user's
   authorization to publish. Never force-push or use text update_file for PNG.
5. After Pages succeeds, download the actual gallery and every referenced PNG.
   Require HTTP 200, correct dimensions and SHA-256 equal to the local manifest.
   Only then write the task's result JSON with status=done and the live URL.
   If any step fails, report the concrete failure; do not ask the user to upload
   a ZIP or pretend publication succeeded.

For task 495, `stories-495-manifest.json` records final checksums and the hashes
of retired legacy ZIPs. The legacy extraction script ignores those archives,
so a manual rerun cannot restore the defective original images. New ZIPs are
still supported for compatibility, but are not part of the automatic path.

No OpenAI API key, GitHub token pasted by the user, or paid upload service is
required by the connector publication path. Image generation still depends on
the tools available during the automation run; missing tools must be reported
as a failure rather than a request for a manual archive.
