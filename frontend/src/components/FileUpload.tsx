import { useState } from "react";
import apiClient from "../../api/client";

function FileUpload() {
  const [file, setFile] = useState<File | null>(
    null
  );

  const uploadFile = async () => {
    if (!file) return;

    const formData = new FormData();

    formData.append("file", file);

    try {
      await apiClient.post(
        "/ingestion/upload/",
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      );

      alert("Upload successful");

      window.location.reload();
    } catch (error) {
      console.error(error);

      alert("Upload failed");
    }
  };

  return (
    <div style={{ marginBottom: "20px" }}>
      <input
        type="file"
        accept=".csv"
        onChange={(e) => {
          if (e.target.files?.[0]) {
            setFile(e.target.files[0]);
          }
        }}
      />

      <button
        onClick={uploadFile}
        style={{ marginLeft: "10px" }}
      >
        Upload CSV
      </button>
    </div>
  );
}

export default FileUpload;