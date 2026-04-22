import Swal from "sweetalert2";
import { TypeNoti } from "../../utils/constants";

export const Notification = ({ type, title }) => {
  return Swal.fire({
    icon: type,
    title: type === TypeNoti.success ? "Thành công" : "Lỗi",
    text: title,
    confirmButtonText: "OK",
    confirmButtonColor: type === TypeNoti.success ? "#198754" : "#dc3545",
    timer: 2000,
    timerProgressBar: true,
  });
};
