import axios from "axios";
import { useEffect, useState } from "react";

export const Account = () => {
  const [listUser, setListUser] = useState([]);
  const [showModal, setShowModal] = useState(false);
  useEffect(() => {
    axios.get("http://localhost:8000/api/accounts").then((res) => {
      setListUser(res.data);
    });
  }, []);

  return (
    <table className="table table-hover align-middle">
      <thead>
        <tr>
          <th width="60">STT</th>
          <th>Username</th>
          <th width="160">Hành động</th>
        </tr>
      </thead>
      <tbody id="intentTable">
        {listUser.map((item, i) => {
          return (
            <tr>
              <td key={i}>{i + 1}</td>
              <td>{item.username}</td>
              <td>
                <button
                  className="btn btn-sm btn-outline-primary me-2"
                  onClick={() => setShowModal(true)}
                >
                  <i className="bi bi-pencil-square"></i> Cập nhật
                </button>
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};
