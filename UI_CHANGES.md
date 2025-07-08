## UI Changes Preview

### Before:
```
[🔍] [Search Box] [刷新账号列表]
```

### After:
```
[🔍] [Search Box] [刷新账号列表] [选择文件夹]
```

### New Button Functionality:
- **Button Text**: "选择文件夹"
- **Action**: Opens directory selection dialog
- **Result**: Updates mafiles_dir and refreshes account list
- **Feedback**: Shows confirmation message with selected path

### Usage Instructions Update:
**Before**: "将所有 Steam maFile 文件放入本程序同目录的 maFile 文件夹内。"
**After**: "将所有 Steam maFile 文件放入 maFiles 文件夹或自定义文件夹。"

### Directory Selection Dialog:
- **Title**: "选择 maFile 文件夹"
- **Type**: Standard folder selection dialog
- **Behavior**: If user selects a folder, it becomes the new mafiles_dir
- **Confirmation**: Shows message "已选择文件夹：[selected_path]"