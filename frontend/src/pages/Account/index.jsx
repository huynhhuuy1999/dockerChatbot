import axios from "axios";
import { useEffect, useState } from "react";
import { Button, Form, Modal } from "react-bootstrap";
import style from "./style.module.scss";

export const Account = () => {
  const [listUser, setListUser] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [currentUserUpdate, setCurrentUserUpdate] = useState({});
  const [isUpdatePassword, setIsUpdatePassword] = useState(false);
  useEffect(() => {
    axios.get("http://localhost:8000/api/accounts").then((res) => {
      setListUser(res.data);
    });
  }, []);

  const onSave = (e) => {
    e.preventDefault();
    const dataUpdate = { ...currentUserUpdate };
    if (isUpdatePassword) {
      dataUpdate.password = currentUserUpdate.newPassword;
    }

    axios
      .post("http://localhost:8000/api/update_account", {
        ...dataUpdate,
        isUpdatePassword: isUpdatePassword,
      })
      .then((res) => {
        if (res.data.status === "success") {
          setShowModal(false);
          // Cập nhật lại danh sách tài khoản sau khi cập nhật thành công
        }
      })
      .catch((err) => {
        if (err.response) {
          // server trả response (401, 400,...)
          const msg = err.response.data.error;
          alert(msg);
        } else {
          // lỗi network (server down, sai URL,...)
          alert("❌ Lỗi kết nối Backend");
        }
      });
  };

  return (
    <>
      <div className={`card ${style.blockTable}`}>
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
                <tr key={i}>
                  <td className="text-center">{i + 1}</td>
                  <td>{item.username}</td>
                  <td>
                    <button
                      className="btn btn-sm btn-outline-primary me-2"
                      onClick={() => {
                        setShowModal(true);
                        setCurrentUserUpdate({
                          ...item,
                          newPassword: "",
                          newUserName: item.username,
                        });
                      }}
                    >
                      <i className="bi bi-pencil-square"></i> Cập nhật
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <Modal
        show={showModal}
        onHide={() => setShowModal(false)}
        size="sm"
        onExit={() => setIsUpdatePassword(false)}
      >
        <Modal.Header closeButton>
          <Modal.Title style={{ fontSize: 18, fontWeight: "bold" }}>
            Cập nhật tài khoản
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div>
            <Form onSubmit={onSave}>
              <Form.Group controlId="formBasicEmail">
                <Form.Control
                  type="text"
                  placeholder="Enter username"
                  required
                  onChange={(e) =>
                    setCurrentUserUpdate({
                      ...currentUserUpdate,
                      newUserName: e.target.value,
                    })
                  }
                  value={currentUserUpdate.newUserName}
                  className="mb-3"
                />
                <Form.Control.Feedback type="invalid">
                  Please provide a valid username.
                </Form.Control.Feedback>
                <Form.Check // prettier-ignore
                  type={"checkbox"}
                  id={`default-checkbox`}
                  label={`Cập nhật mật khẩu`}
                  value={isUpdatePassword}
                  onChange={(e) => setIsUpdatePassword(e.target.checked)}
                />
                <Form.Control
                  type="password"
                  placeholder="Enter password"
                  required
                  onChange={(e) =>
                    setCurrentUserUpdate({
                      ...currentUserUpdate,
                      newPassword: e.target.value,
                    })
                  }
                  className="mb-3"
                  value={currentUserUpdate.newPassword}
                  disabled={!isUpdatePassword}
                />
                <Form.Control.Feedback type="invalid">
                  Please provide a valid password.
                </Form.Control.Feedback>
              </Form.Group>
              <div className={style.groupButton}>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => setShowModal(false)}
                >
                  Đóng
                </Button>
                <Button
                  variant="primary"
                  size="sm"
                  className="ms-2"
                  type="submit"
                >
                  Lưu thay đổi
                </Button>
              </div>
            </Form>
          </div>
        </Modal.Body>
        <Modal.Footer></Modal.Footer>
      </Modal>
    </>
  );
};
