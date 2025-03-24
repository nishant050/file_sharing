import os
import streamlit as st
import mimetypes
import base64

# Persistent storage configuration
UPLOAD_FOLDER = 'shared_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_file_type(filename):
    """Determine the type of file for preview"""
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type

def list_files():
    """List all files in the shared directory"""
    return os.listdir(UPLOAD_FOLDER)

def delete_file(filename):
    """Delete a specific file"""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

def preview_file(filename):
    """Generate preview for supported file types"""
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    mime_type = get_file_type(filename)

    # Image preview
    if mime_type and mime_type.startswith('image/'):
        with open(file_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode()
        st.image(f'data:{mime_type};base64,{image_data}')

    # Video preview
    elif mime_type and mime_type.startswith('video/'):
        with open(file_path, 'rb') as f:
            video_data = base64.b64encode(f.read()).decode()
        st.video(f'data:{mime_type};base64,{video_data}')

    # Text file preview
    elif mime_type and mime_type.startswith('text/'):
        with open(file_path, 'r') as f:
            st.text(f.read())

def main():
    st.title('Advanced File Sharing Platform')

    # Upload Section
    st.header('📤 Upload Files')
    uploaded_file = st.file_uploader('Choose a file to upload', accept_multiple_files=False)
    
    if uploaded_file is not None:
        # Save the uploaded file permanently
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.success(f'File {uploaded_file.name} uploaded successfully!')

    # File Management Section
    st.header('📁 File Management')
    
    # List available files
    available_files = list_files()
    
    if available_files:
        # File selection
        col1, col2 = st.columns(2)
        
        with col1:
            selected_file = st.selectbox('Choose a file', available_files)
        
        with col2:
            # Action buttons
            col_preview, col_download, col_delete = st.columns(3)
            
            with col_preview:
                preview_button = st.button('Preview')
            
            with col_download:
                download_button = st.download_button(
                    label='Download',
                    data=open(os.path.join(UPLOAD_FOLDER, selected_file), 'rb').read(),
                    file_name=selected_file,
                    mime='application/octet-stream'
                )
            
            with col_delete:
                delete_button = st.button('Delete')
        
        # Preview handling
        if preview_button:
            try:
                preview_file(selected_file)
            except Exception as e:
                st.error(f"Cannot preview file: {e}")
        
        # Delete handling
        if delete_button:
            if delete_file(selected_file):
                st.success(f'File {selected_file} deleted successfully!')
                st.experimental_rerun()
            else:
                st.error('Failed to delete file')
    
    else:
        st.write('No files available')

if __name__ == '__main__':
    main()