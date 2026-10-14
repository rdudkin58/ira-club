// Run this file in functions.exec after storing image_upload_inputs.
// Inputs: { repository, helper (absolute binary_chunk.py path),
//           files: [{local_path, path, git_blob_sha}] }
// Outputs: image_upload_tree_elements. No local credentials or manual ZIP.
const inputs = load('image_upload_inputs');
if (!inputs || !inputs.files?.length) throw new Error('Missing image_upload_inputs');
const quote = s => "'" + String(s).replaceAll("'", "'\\''") + "'";
const entries = [];
for (const file of inputs.files) {
  let offset = 0, base64 = '';
  while (true) {
    const result = await tools.exec_command({
      cmd: `python3 ${quote(inputs.helper)} ${quote(file.local_path)} --offset ${offset}`,
      max_output_tokens: 150000
    });
    if (result.exit_code !== 0) throw new Error('Cannot read ' + file.path);
    const chunk = JSON.parse(result.output);
    base64 += chunk.base64;
    offset += chunk.bytes;
    if (offset === chunk.total) break;
    if (!chunk.bytes || offset > chunk.total) throw new Error('Invalid chunk sequence');
  }
  const response = await tools.mcp__codex_apps__github_create_blob({
    repository_full_name: inputs.repository, content: base64, encoding: 'base64'
  });
  if (response.isError) throw new Error(JSON.stringify(response));
  const sha = response.structuredContent?.sha;
  if (!sha || sha !== file.git_blob_sha) throw new Error('Blob byte verification failed: ' + file.path);
  entries.push({path: file.path, mode: '100644', type: 'blob', sha});
  store('image_upload_tree_elements', entries);
  text({uploaded: file.path, sha, bytes: offset});
}
