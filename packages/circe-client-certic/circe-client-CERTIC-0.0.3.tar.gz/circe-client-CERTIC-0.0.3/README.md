# Circe Python Client

```
from circe_client import Client

client = Client()
job = client.new_job()
job.add_file("doc.docx")
job.add_transformation("donothing")
client.send(job, wait=True)
for file_name, file_pointer in job.result.files:
    pass  # do something with result files
```