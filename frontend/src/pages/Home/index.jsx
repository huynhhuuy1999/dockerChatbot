import { useState, useEffect } from "react";
import style from "./home.module.scss";
import axios from "axios";
import { Button, Modal, Pagination } from "react-bootstrap";
import Swal from "sweetalert2";
export const Home = () => {
  const [listIntent, setListIntent] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = listIntent.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(listIntent.length / itemsPerPage);
  const [currentDataUpdate, setCurrentDataUpdate] = useState({});
  const [show, setShow] = useState(false);

  const renderPaginationItems = () => {
    let items = [];
    for (let number = 1; number <= totalPages; number++) {
      items.push(
        <Pagination.Item
          key={number}
          active={number === currentPage}
          onClick={() => setCurrentPage(number)}
        >
          {number}
        </Pagination.Item>,
      );
    }
    return items;
  };

  const openModal = (index) => {
    setShow(true);
    setCurrentDataUpdate(listIntent[index]);
    const data = listIntent[index];
    console.log("data", data);
  };

  const onSave = () => {
    const dataToSend = {
      intent: currentDataUpdate.intent,
      entities: currentDataUpdate.entities.map((e) => ({
        entity: e.entity_name,
        answer: e.answer || "",
      })),
    };

    fetch("http://localhost:8000/api/update", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dataToSend),
    })
      .then((res) => res.json())
      .then((resp) => {
        if (resp.status === "success") {
          setShow(false);
          // Hiển thị alert đẹp với SweetAlert2
          Swal.fire({
            icon: "success",
            title: "Cập nhật thành công",
            text: "Answer đã được lưu vào hệ thống",
            confirmButtonText: "OK",
            confirmButtonColor: "#198754",
            timer: 2000,
            timerProgressBar: true,
          });
        } else {
          Swal.fire({
            icon: "error",
            title: "Lỗi",
            text: "Không thể lưu dữ liệu!",
          });
        }
      })
      .catch((err) => {
        console.error(err);
        Swal.fire({
          icon: "error",
          title: "Lỗi mạng",
          text: "Không thể kết nối tới server!",
        });
      });
  };

  useEffect(() => {
    axios.get("http://localhost:8000/api/intents").then((res) => {
      setListIntent(res.data);
    });
  }, []);

  return (
    <>
      <div className="mb-3">
        <input
          type="text"
          id="searchInput"
          className="form-control"
          placeholder="🔍 Tìm kiếm Intent..."
          onkeyup="searchIntent()"
        />
      </div>

      <div className={`${style.card} card`}>
        <div className="card-body">
          <table className="table table-hover align-middle">
            <thead>
              <tr>
                <th width="60">STT</th>
                <th>Intent</th>
                <th width="160">Hành động</th>
              </tr>
            </thead>
            <tbody id="intentTable">
              {currentItems.map((item, i) => {
                return (
                  <tr key={i}>
                    <td>{indexOfFirstItem + i + 1}</td>
                    <td>{item.intent}</td>
                    <td>
                      <button
                        class="btn btn-sm btn-outline-primary"
                        // onClick="openModal(${i})"
                        onClick={() => openModal(i)}
                      >
                        <i class="bi bi-pencil-square"></i> Cập nhật
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <Pagination>
            <Pagination.Prev
              disabled={currentPage === 1}
              onClick={() => setCurrentPage(currentPage - 1)}
            />

            {renderPaginationItems()}

            <Pagination.Next
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage(currentPage + 1)}
            />
          </Pagination>
        </div>
      </div>

      <Modal show={show} onHide={() => setShow(false)} size="xl">
        <Modal.Header closeButton>
          <Modal.Title style={{ fontSize: 18, fontWeight: "bold" }}>
            Cập nhật câu trả lời
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <input
            id="modalIntent"
            className="form-control mb-3"
            value={currentDataUpdate.intent}
            disabled
          />
          <div className={style.bodyTable}>
            {currentDataUpdate.entities &&
              currentDataUpdate.entities.map((item, i) => (
                <div className={`border p-3 mb-3 rounded`} key={i}>
                  {item.entity_text || item.entity_name ? (
                    <label>
                      <b>Entity:</b> {item.entity_text || item.entity_name}
                    </label>
                  ) : (
                    ""
                  )}
                  <textarea
                    className="form-control mt-2"
                    rows="6"
                    onChange={(e) => {
                      const newEntities = [...currentDataUpdate.entities];
                      newEntities[i].answer = e.target.value;
                      setCurrentDataUpdate({
                        ...currentDataUpdate,
                        entities: newEntities,
                      });
                    }}
                    value={item.answer || ""}
                  ></textarea>
                </div>
              ))}
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" size="sm" onClick={() => setShow(false)}>
            Đóng
          </Button>
          <Button variant="primary" size="sm" onClick={onSave}>
            Lưu thay đổi
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};
