import os
import streamlit as st
import mimetypes
import urllib.parse

# Persistent storage configuration
UPLOAD_FOLDER = 'shared_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class FileManager:
    @staticmethod
    def generate_file_url(filename):
        """Generate a simple shareable URL for the file"""
        return f"http://localhost:8501/download/{urllib.parse.quote(filename)}"

    @staticmethod
    def list_files():
        """List all files in the shared directory"""
        return os.listdir(UPLOAD_FOLDER)

def main():
    st.title('Simple File Sharing Platform')

    # Upload Section
    st.header('Upload Files')
    uploaded_file = st.file_uploader('Choose a file to upload', accept_multiple_files=False)
    
    if uploaded_file is not None:
        # Save the uploaded file permanently
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        # Generate file URL
        file_url = FileManager.generate_file_url(uploaded_file.name)
        
        # Display success and URL
        st.success(f'File {uploaded_file.name} uploaded successfully!')
        st.write('Shareable URL:')
        st.code(file_url)

    # File Management Section
    st.header('Uploaded Files')
    
    # List available files
    available_files = FileManager.list_files()
    
    if available_files:
        for filename in available_files:
            col1, col2 = st.columns(2)
            
            with col1:
                # Download Button
                with open(os.path.join(UPLOAD_FOLDER, filename), 'rb') as f:
                    st.download_button(
                        label='Download',
                        data=f.read(),
                        file_name=filename,
                        mime='application/octet-stream'
                    )
            
            with col2:
                # Show shareable URL
                st.write('Shareable URL:')
                st.code(FileManager.generate_file_url(filename))
    
    else:
        st.write('No files available')

if __name__ == '__main__':
    main()