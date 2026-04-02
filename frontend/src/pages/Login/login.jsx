import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import style from "./login.module.scss";
export const Login = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState("");
  const [pass, setPass] = useState("");
  const onLogin = () => {
    axios
      .post("http://localhost:8000/api/login", {
        username: user,
        password: pass,
      })
      .then((res) => {
        if (res.data.status === "success") {
          localStorage.setItem("admin_login", "true");
          navigate("/");
        } else {
          alert("❌ Sai tài khoản hoặc mật khẩu");
        }
      })
      .catch((err) => {
        alert("❌ Lỗi kết nối Backend");
        console.error(err);
      });
  };
  return (
    <div className={`${style.loginBody}`}>
      <div className={`${style.card} shadow`}>
        <h4 className="text-center mb-3">Admin</h4>

        <input
          value={user}
          class="form-control mb-3"
          placeholder="Username"
          onChange={(e) => setUser(e.target.value)}
        />
        <input
          value={pass}
          id="pass"
          type="password"
          class="form-control mb-4"
          placeholder="Password"
          onChange={(e) => setPass(e.target.value)}
        />

        <button class="btn btn-primary w-100" onClick={onLogin}>
          Đăng nhập
        </button>

        <div id="msg" class="text-danger mt-3 text-center"></div>
      </div>
    </div>
  );
};
