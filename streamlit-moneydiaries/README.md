If you're running streamlit from a remote machine and want to access the dashboard you will need to create an ssh tunnel to the remote server. You can use the following command (replace username and ip by the relevant values)

```bash
ssh -N -L localhost:8501:localhost:8501 username@ip
```