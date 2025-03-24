import os
import streamlit as st
import mimetypes
import base64
import urllib.parse

# Persistent storage configuration
UPLOAD_FOLDER = 'shared_files'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class FileManager:
    @staticmethod
    def generate_file_url(filename):
        """Generate a shareable direct download URL"""
        return f"https://nishantshares.streamlit.app/download/{urllib.parse.quote(filename)}"

    @staticmethod
    def get_file_details(filename):
        """Get detailed information about the file"""
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file_size = os.path.getsize(file_path)
        mime_type, _ = mimetypes.guess_type(filename)
        
        return {
            'name': filename,
            'size': f"{file_size / 1024:.2f} KB",
            'type': mime_type or 'Unknown'
        }

    @staticmethod
    def generate_sharing_links(file_url, filename):
        """Generate sharing links for different platforms"""
        encoded_message = urllib.parse.quote(f"Check out this file: {file_url}")
        
        return {
            'WhatsApp': f"https://wa.me/?text={encoded_message}",
            'Email': f"mailto:?subject=Shared File: {filename}&body={encoded_message}",
            'Teams': f"https://teams.microsoft.com/l/chat/0/0?users=&message={encoded_message}"
        }

    @staticmethod
    def preview_file(filename):
        """Generate preview for supported file types"""
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        mime_type, _ = mimetypes.guess_type(filename)

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
        
        else:
            st.warning("File type not supported for preview")

def main():
    st.title('File Sharing Platform')

    # File Upload Section
    st.header('📤 Upload Files')
    uploaded_file = st.file_uploader('Choose a file to upload', accept_multiple_files=False)
    
    if uploaded_file is not None:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.success(f'File {uploaded_file.name} uploaded successfully!')

    # File Management Section
    st.header('📁 Uploaded Files')
    
    # List files
    files = os.listdir(UPLOAD_FOLDER)
    
    if files:
        for filename in files:
            with st.expander(filename):
                # File Details
                file_details = FileManager.get_file_details(filename)
                st.json(file_details)

                # Preview Section
                st.subheader('Preview')
                try:
                    FileManager.preview_file(filename)
                except Exception as e:
                    st.error(f"Preview not available: {e}")

                # Download Section
                col1, col2 = st.columns(2)
                
                with col1:
                    # Download Button
                    with open(os.path.join(UPLOAD_FOLDER, filename), 'rb') as f:
                        st.download_button(
                            label='Download File',
                            data=f.read(),
                            file_name=filename,
                            mime='application/octet-stream'
                        )
                
                with col2:
                    # Direct Download Link
                    file_url = FileManager.generate_file_url(filename)
                    st.subheader('Direct Download Link')
                    st.code(file_url)
                    
                    # Copy URL Button
                    if st.button(f'Copy URL for {filename}'):
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
                sharing_links = FileManager.generate_sharing_links(file_url, filename)
                
                # Create columns for sharing buttons
                share_cols = st.columns(len(sharing_links))
                for col, (platform, share_url) in zip(share_cols, sharing_links.items()):
                    with col:
                        st.markdown(f'[Share via {platform}]({share_url})', unsafe_allow_html=True)
    
    else:
        st.write('No files uploaded yet')

if __name__ == '__main__':
    main()