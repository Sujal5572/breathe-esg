import { useEffect, useState } from "react";
import apiClient from "../../api/client";
import FileUpload from "../components/FileUpload";

interface RecordItem {
  id: number;
  activity_type: string;
  facility: string;
  quantity: string;
  normalized_unit: string;
  suspicious: boolean;
  review_status: string;
}

function ReviewQueuePage() {
  const [records, setRecords] = useState<RecordItem[]>([]);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    fetchRecords();
  }, []);

  const fetchRecords = async () => {
    try {
      const response = await apiClient.get(
        "/records/"
      );

      setRecords(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const approveRecord = async (id: number) => {
    try {
      await apiClient.post(
        `/records/${id}/approve/`
      );

      fetchRecords();
    } catch (error) {
      console.error(error);
    }
  };

  const rejectRecord = async (id: number) => {
    try {
      await apiClient.post(
        `/records/${id}/reject/`
      );

      fetchRecords();
    } catch (error) {
      console.error(error);
    }
  };
  const filteredRecords = records.filter((record) => {
      if (filter === "pending") {
        return record.review_status === "pending";
      }

      if (filter === "approved") {
        return record.review_status === "approved";
      }

      if (filter === "suspicious") {
        return record.suspicious === true;
      }

      return true;
    });

  return (
    <div style={{ padding: "20px" }}>
      <h1>Review Queue</h1>
      <FileUpload/>
      <div style={{ marginBottom: "20px" }}>
          <button onClick={() => setFilter("all")}>
            All
          </button>

          <button
            onClick={() => setFilter("pending")}
            style={{ marginLeft: "10px" }}
          >
            Pending
          </button>

          <button
            onClick={() => setFilter("suspicious")}
            style={{ marginLeft: "10px" }}
          >
            Suspicious
          </button>

          <button
            onClick={() => setFilter("approved")}
            style={{ marginLeft: "10px" }}
          >
            Approved
          </button>
        </div>

      <table
        border={1}
        cellPadding={10}
        style={{
          borderCollapse: "collapse",
          width: "100%",
        }}
      >
        <thead>
          <tr>
            <th>ID</th>
            <th>Activity</th>
            <th>Facility</th>
            <th>Quantity</th>
            <th>Suspicious</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {filteredRecords.map((record) => (
            <tr key={record.id}>
              <td>{record.id}</td>

              <td>
                {record.activity_type}
              </td>

              <td>{record.facility}</td>

              <td>
                {record.quantity}{" "}
                {record.normalized_unit}
              </td>

              <td>
                {record.suspicious
                  ? "⚠️ Yes"
                  : "No"}
              </td>

              <td>
                {record.review_status}
              </td>

              <td>
                {record.review_status === "pending" ? (
                  <>
                    <button
                      onClick={() =>
                        approveRecord(record.id)
                      }
                    >
                      Approve
                    </button>

                    <button
                      onClick={() =>
                        rejectRecord(record.id)
                      }
                      style={{
                        marginLeft: "10px",
                      }}
                    >
                      Reject
                    </button>
                  </>
                ) : (
                  <span>Completed</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ReviewQueuePage;