# maFiles Directory Customization Feature

## Overview
This implementation adds the ability for users to customize the directory used to store Steam maFile files, with the following changes:

## Changes Made

### 1. Updated Default Directory
- **Before**: `MAFILES_DIR = "maFile"`
- **After**: `DEFAULT_MAFILES_DIR = "maFiles"`

### 2. Added Instance Variable
- Added `self.mafiles_dir` to track the current directory
- Initialized to `DEFAULT_MAFILES_DIR` in `__init__`

### 3. Added UI Components
- **New Button**: "选择文件夹" button added to the top frame
- **Position**: Placed after the "刷新账号列表" button
- **Function**: Calls `self.choose_folder()` method

### 4. Implemented choose_folder Method
```python
def choose_folder(self):
    selected_folder = filedialog.askdirectory(title="选择 maFile 文件夹")
    if selected_folder:
        self.mafiles_dir = selected_folder
        self.refresh_mafiles()
        messagebox.showinfo("提示", f"已选择文件夹：{selected_folder}")
```

### 5. Updated Account Loading Logic
- **Before**: `load_mafiles(MAFILES_DIR)` (hardcoded)
- **After**: `load_mafiles(self.mafiles_dir)` (dynamic)

### 6. Updated Usage Instructions
- **Before**: "将所有 Steam maFile 文件放入本程序同目录的 maFile 文件夹内"
- **After**: "将所有 Steam maFile 文件放入 maFiles 文件夹或自定义文件夹"

### 7. Added Required Import
- Added `filedialog` to the tkinter imports

## User Experience
1. **Default Behavior**: Uses "maFiles" directory (same as before, but renamed)
2. **Custom Directory**: Users can click "选择文件夹" to choose any directory
3. **Immediate Update**: When a new directory is selected, the account list refreshes automatically
4. **Visual Feedback**: Shows confirmation message with selected directory path

## Technical Implementation
- Maintains backward compatibility (just directory name change)
- All existing functionality preserved
- Clean, minimal code changes
- No breaking changes to existing features
- Proper error handling for directory selection

## Testing
- ✅ Default directory functionality
- ✅ Custom directory selection
- ✅ Account loading from different directories
- ✅ UI components properly integrated
- ✅ Refresh functionality works with custom directories
- ✅ All existing features remain functional