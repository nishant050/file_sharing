import os
import streamlit as st
import mimetypes
import base64
import urllib.parse

# Persistent storage configuration
UPLOAD_FOLDER = 'shared_files'
BASE_URL = st.secrets.get('BASE_URL', 'http://localhost:8501/download/')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class FileManager:
    @staticmethod
    def generate_file_url(filename):
        """Generate a unique, shareable URL for the file"""
        # URL encode the filename to handle special characters
        encoded_filename = urllib.parse.quote(filename)
        return f"{BASE_URL}{encoded_filename}"

    @staticmethod
    def list_files():
        """List all files in the shared directory"""
        return os.listdir(UPLOAD_FOLDER)

    @staticmethod
    def get_file_details(filename):
        """Get file details including size and type"""
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file_size = os.path.getsize(file_path)
        mime_type, _ = mimetypes.guess_type(filename)
        return {
            'name': filename,
            'size': f"{file_size / 1024:.2f} KB",
            'type': mime_type or 'Unknown'
        }

    @staticmethod
    def generate_sharing_options(file_url, filename):
        """Generate sharing options for different platforms"""
        # URL encode the message for different sharing platforms
        encoded_message = urllib.parse.quote(f"Check out this file: {file_url}")
        
        sharing_options = {
            'WhatsApp': f"https://wa.me/?text={encoded_message}",
            'Email': f"mailto:?body={encoded_message}",
            'Telegram': f"https://t.me/share/url?url={file_url}&text={filename}",
        }
        
        return sharing_options

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
        
        # Generate file URL
        file_url = FileManager.generate_file_url(uploaded_file.name)
        
        # Display success and URL
        st.success(f'File {uploaded_file.name} uploaded successfully!')
        st.subheader('File Sharing Options')
        
        # File Details
        file_details = FileManager.get_file_details(uploaded_file.name)
        st.json(file_details)
        
        # Direct Download URL
        st.markdown(f"**Direct Download URL:**\n`{file_url}`")
        st.code(file_url, language='text')
        
        # Copy URL Button
        copy_url_button = st.button('Copy URL to Clipboard')
        if copy_url_button:
            st.toast('URL Copied to Clipboard!')
            st.components.v1.html(
                f"""
                <script>
                    navigator.clipboard.writeText('{file_url}');
                </script>
                """,
                height=0
            )
        
        # Sharing Options
        st.subheader('Share File')
        sharing_options = FileManager.generate_sharing_options(file_url, uploaded_file.name)
        
        # Create columns for sharing buttons
        cols = st.columns(len(sharing_options))
        for col, (platform, share_url) in zip(cols, sharing_options.items()):
            with col:
                st.markdown(f'[Share via {platform}]({share_url})', unsafe_allow_html=True)

    # File Management Section
    st.header('📁 Uploaded Files')
    
    # List available files
    available_files = FileManager.list_files()
    
    if available_files:
        for filename in available_files:
            with st.expander(filename):
                # File details
                file_details = FileManager.get_file_details(filename)
                st.json(file_details)
                
                # Generate file URL
                file_url = FileManager.generate_file_url(filename)
                
                # Download and Share columns
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
                    # Share Button
                    sharing_options = FileManager.generate_sharing_options(file_url, filename)
                    platform = st.selectbox(f'Share {filename} via', list(sharing_options.keys()), key=filename)
                    st.markdown(f'[Share]({sharing_options[platform]})', unsafe_allow_html=True)
    
    else:
        st.write('No files available')

if __name__ == '__main__':
    main()