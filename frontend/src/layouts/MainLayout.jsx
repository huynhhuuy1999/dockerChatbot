import { NavLink, Outlet, useLocation } from "react-router-dom";
import style from "./style.module.scss";
import { Button, Modal } from "react-bootstrap";
import { useEffect, useState } from "react";

const listAction = [
  { path: "/", name: "Quản lý Answer", title: "Cập nhật câu trả lời" },
  { path: "/accounts", name: "Quản lý tài khoản", title: "Quản lý tài khoản" },
];

export const MainLayout = () => {
  const location = useLocation();
  const path = location.pathname;
  const [show, setShow] = useState(false);
  const [title, setTitle] = useState("Cập nhật câu trả lời");

  useEffect(() => {
    const isLogin = localStorage.getItem("admin_login");
    if (!isLogin) {
      // window.location.href = "/login";
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("admin_login");
    setShow(false);
    window.location.href = "/login";
  };

  return (
    <div className={style.bodyHome}>
      <div className={style.sidebar}>
        <div>
          <div className={style.logo}>ADMIN</div>
          {listAction.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={`${path === item.path ? style.active : ""} ${style.link}`}
              onClick={() => setTitle(item.title)}
            >
              <i className="bi bi-chat-left-text"></i> {item.name}
            </NavLink>
          ))}
        </div>
        <div className={style.logout}>
          <button className="btn btn-danger w-75" onClick={() => setShow(true)}>
            Đăng xuất
          </button>
        </div>
      </div>
      <div className={style.main}>
        <div
          className={
            style.header + " d-flex justify-content-between align-items-center"
          }
        >
          <h5 className="mb-0">{title}</h5>
        </div>
        <Outlet />
      </div>
      <Modal show={show} onHide={() => setShow(false)}>
        <Modal.Header closeButton>
          <Modal.Title style={{ fontSize: 18, fontWeight: "bold" }}>
            Cập nhật câu trả lời
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p className="mb-0">
            Bạn có chắc chắn muốn <strong>đăng xuất khỏi hệ thống</strong>{" "}
            không?
          </p>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" size="sm" onClick={() => setShow(false)}>
            Đóng
          </Button>
          <Button variant="danger" size="sm" onClick={handleLogout}>
            Đăng xuất
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};
