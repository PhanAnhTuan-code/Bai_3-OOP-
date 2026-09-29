# MSSV: 20227207
# Họ tên: Phan Anh Tuấn

import math
from typing import List, Optional
 
 
# ---------------------------------------------------------------- tiện ích kiểm tra
def _require_text(value, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field} phải là chuỗi")
    value = value.strip()
    if not value:
        raise ValueError(f"{field} không được rỗng")
    return value
 
 
def _require_money(value, field: str, allow_zero: bool = True) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field} phải là số")
    if math.isnan(value) or math.isinf(value):
        raise ValueError(f"{field} phải là số hữu hạn")
    if value < 0 or (value == 0 and not allow_zero):
        raise ValueError(f"{field} phải {'không âm' if allow_zero else 'dương'}")
    return float(value)
 
 
# ---------------------------------------------------------------------- Employee
class Employee:
    """Nhân sự thông thường."""
 
    def __init__(self, id: str = "UNKNOWN", full_name: str = "Unnamed employee",
                 base_salary: float = 0):
        # Employee() | Employee(id, name) | Employee(id, name, salary)
        self._id = _require_text(id, "Mã nhân sự")
        self._full_name = _require_text(full_name, "Họ tên")
        self._base_salary = _require_money(base_salary, "Lương cơ bản")
 
    # getter
    @property
    def id(self) -> str:
        return self._id
 
    @property
    def full_name(self) -> str:
        return self._full_name
 
    @property
    def base_salary(self) -> float:
        return self._base_salary
 
    # nạp chồng increaseSalary
    def increase_salary(self, value: float, by_percentage: Optional[bool] = None) -> None:
        """
        increase_salary(amount)                 -> tăng số tiền cố định
        increase_salary(value, by_percentage)   -> True: tăng theo %, False: số tiền cố định
        """
        value = _require_money(value, "Giá trị tăng", allow_zero=False)
        if by_percentage:  # True
            self._base_salary += self._base_salary * value / 100.0
        else:              # None (phiên bản 1) hoặc False
            self._base_salary += value
 
    def calculate_monthly_cost(self) -> float:
        return self._base_salary
 
    def display_info(self) -> None:
        print(f"[Employee] {self._id} | {self._full_name} | "
              f"lương cơ bản: {self._base_salary:,.2f} | chi phí tháng: {self.calculate_monthly_cost():,.2f}")
 
    def __del__(self):
        # dùng getattr phòng trường hợp constructor ném lỗi giữa chừng
        print(f"  (~Employee) Hủy nhân sự {getattr(self, '_id', '?')}")
 
 
# ------------------------------------------------------------- SoftwareEngineer
class SoftwareEngineer(Employee):
    """Kỹ sư phần mềm."""
 
    def __init__(self, id: str, full_name: str, *args):
        """
        SoftwareEngineer(id, name, primary_language)
        SoftwareEngineer(id, name, base_salary, primary_language, technical_allowance)
        """
        if len(args) == 1:
            base_salary, language, allowance = 0, args[0], 0
        elif len(args) == 3:
            base_salary, language, allowance = args
        else:
            raise TypeError("SoftwareEngineer nhận (id, name, language) hoặc "
                            "(id, name, salary, language, allowance)")
        language = _require_text(language, "Ngôn ngữ lập trình chính")
        allowance = _require_money(allowance, "Phụ cấp kỹ thuật")
        super().__init__(id, full_name, base_salary)
        self._primary_language = language
        self._technical_allowance = allowance
 
    @property
    def primary_language(self) -> str:
        return self._primary_language
 
    @property
    def technical_allowance(self) -> float:
        return self._technical_allowance
 
    def calculate_monthly_cost(self) -> float:
        return self._base_salary + self._technical_allowance
 
    def display_info(self) -> None:
        print(f"[SoftwareEngineer] {self._id} | {self._full_name} | "
              f"lương cơ bản: {self._base_salary:,.2f} | ngôn ngữ: {self._primary_language} | "
              f"phụ cấp: {self._technical_allowance:,.2f} | chi phí tháng: {self.calculate_monthly_cost():,.2f}")
 
    def __del__(self):
        print(f"  (~SoftwareEngineer) Hủy kỹ sư {getattr(self, '_id', '?')}")
        super().__del__()
 
 
# ------------------------------------------------------------------ ProjectTeam
class ProjectTeam:
    """Nhóm dự án: liên kết KHÔNG sở hữu tới Employee."""
 
    def __init__(self, project_code: str, project_name: str,
                 leader: Optional[Employee] = None):
        # ProjectTeam(code, name) | ProjectTeam(code, name, leader)
        self._project_code = _require_text(project_code, "Mã dự án")
        self._project_name = _require_text(project_name, "Tên dự án")
        self._members: List[Employee] = []
        self._leader: Optional[Employee] = None
        if leader is not None:
            self._check_employee(leader)
            self._members.append(leader)   # tự đưa trưởng nhóm vào danh sách
            self._leader = leader
 
    @staticmethod
    def _check_employee(employee) -> None:
        if not isinstance(employee, Employee):
            raise TypeError("Đối số phải là một Employee")
 
    @property
    def project_code(self) -> str:
        return self._project_code
 
    @property
    def project_name(self) -> str:
        return self._project_name
 
    @property
    def leader(self) -> Optional[Employee]:
        return self._leader
 
    @property
    def size(self) -> int:
        return len(self._members)
 
    def contains(self, employee_id: str) -> bool:
        return any(m.id == employee_id for m in self._members)
 
    def _find(self, employee_id: str) -> Optional[Employee]:
        return next((m for m in self._members if m.id == employee_id), None)
 
    # nạp chồng addMember
    def add_member(self, employee: Employee, make_leader: bool = False) -> bool:
        """
        add_member(emp)         -> thêm thành viên; False nếu trùng (cùng đối tượng hoặc cùng mã)
        add_member(emp, True)   -> thêm (nếu chưa có) và đặt làm trưởng nhóm
        """
        self._check_employee(employee)
        already = self.contains(employee.id)
        if already and self._find(employee.id) is not employee:
            return False          # khác đối tượng nhưng trùng mã (I3)
        if not make_leader:
            if already:
                return False      # trùng nhân sự (I5)
            self._members.append(employee)
            return True
        # make_leader == True
        if not already:
            self._members.append(employee)
        if self._leader is employee:
            return already is False  # đã là trưởng nhóm: không thay đổi gì
        self._leader = employee      # trưởng nhóm cũ vẫn là thành viên
        return True
 
    def remove_member(self, employee_id: str) -> bool:
        target = self._find(employee_id)
        if target is None:
            return False
        if target is self._leader:
            return False          # I6: phải đổi trưởng nhóm trước
        self._members.remove(target)
        return True
 
    def change_leader(self, employee: Employee) -> bool:
        self._check_employee(employee)
        if self._leader is employee:
            return False
        return self.add_member(employee, True)
 
    def calculate_total_monthly_cost(self) -> float:
        # trưởng nhóm nằm trong members nên không bị tính hai lần
        return sum(m.calculate_monthly_cost() for m in self._members)
 
    def display_team(self) -> None:
        print(f"=== Nhóm {self._project_code}: {self._project_name} ===")
        print("Trưởng nhóm:", self._leader.full_name if self._leader else "(chưa có)")
        if not self._members:
            print("  (chưa có thành viên)")
        for m in self._members:
            tag = " (trưởng nhóm)" if m is self._leader else ""
            m.display_info()          # gọi đa hình
            if tag:
                print("   ^" + tag)
        print(f"Tổng chi phí tháng: {self.calculate_total_monthly_cost():,.2f}")
 
    def __del__(self):
        print(f"  (~ProjectTeam) Hủy nhóm {getattr(self, '_project_code', '?')} "
              f"- chỉ giải phóng danh sách liên kết, KHÔNG hủy Employee")
        if hasattr(self, "_members"):
            self._members.clear()
        self._leader = None
 
 
# ------------------------------------------------------------------------ kiểm thử
def expect_error(exc, func, *a, **k):
    try:
        func(*a, **k)
    except exc as e:
        print(f"   OK - bắt được {type(e).__name__}: {e}")
    else:
        raise AssertionError("Lẽ ra phải có lỗi")
 
 
def check(cond, msg):
    print(("   PASS: " if cond else "   FAIL: ") + msg)
    assert cond, msg
 
 
def test_edge_cases():
    print("\n--- Các trường hợp biên ---")
    expect_error(ValueError, Employee, "", "An")
    expect_error(ValueError, Employee, "E1", "   ")
    expect_error(ValueError, Employee, "E1", "An", -1)
    expect_error(ValueError, Employee, "E1", "An", float("nan"))
    expect_error(TypeError, Employee, "E1", "An", True)
    expect_error(ValueError, SoftwareEngineer, "S1", "Bình", "")
    expect_error(ValueError, SoftwareEngineer, "S1", "Bình", 1000, "C++", -5)
    expect_error(TypeError, SoftwareEngineer, "S1", "Bình")
    e = Employee("E9", "Test", 100)
    expect_error(ValueError, e.increase_salary, 0)
    expect_error(ValueError, e.increase_salary, -10, True)
    expect_error(ValueError, e.increase_salary, 0, True)
    e.increase_salary(50, False)
    check(e.base_salary == 150, "increase_salary(50, False) tăng cố định")
    t = ProjectTeam("T0", "Rỗng")
    check(t.remove_member("khong-co") is False, "xóa nhân sự không tồn tại -> False")
    check(t.calculate_total_monthly_cost() == 0, "nhóm rỗng có tổng chi phí 0")
    check(t.add_member(e) is True and t.add_member(Employee("E9", "Trùng mã")) is False,
          "từ chối nhân sự khác đối tượng nhưng trùng mã")
    expect_error(TypeError, t.add_member, None)
    expect_error(ValueError, ProjectTeam, "", "x")
    t.add_member(e, True)
    check(t.add_member(e, True) is False, "đặt lại chính trưởng nhóm hiện tại -> False")
    check(t.change_leader(e) is False, "change_leader chính trưởng nhóm -> False")
 
 
def local_block(shared_employee: Employee):
    """Nhóm thứ hai chỉ sống trong hàm này."""
    team2 = ProjectTeam("PRJ-02", "Ứng dụng di động")
    check(team2.add_member(shared_employee), "thêm nhân sự đã có ở nhóm 1 vào nhóm 2")
    team2.display_team()
    print("   -> kết thúc khối lệnh cục bộ, nhóm 2 sắp bị hủy ...")
 
 
def main():
    print("1. Tạo hai Employee bằng hai constructor khác nhau")
    emp1 = Employee()
    emp2 = Employee("E002", "Trần Thị B", 12_000_000)
    emp1.display_info()
    emp2.display_info()
 
    print("\n2. Tạo hai SoftwareEngineer bằng hai constructor khác nhau")
    se1 = SoftwareEngineer("S001", "Lê Văn C", "Python")
    se2 = SoftwareEngineer("S002", "Phạm Thị D", 20_000_000, "C++", 3_000_000)
    se1.display_info()
    se2.display_info()
 
    print("\n3. Tăng lương cố định")
    emp2.increase_salary(1_000_000)
    check(emp2.base_salary == 13_000_000, "E002 = 13,000,000")
 
    print("\n4. Tăng lương theo phần trăm")
    se2.increase_salary(10, True)
    check(se2.base_salary == 22_000_000, "S002 tăng 10% = 22,000,000")
 
    print("\n5. Tạo nhóm không có trưởng nhóm")
    team = ProjectTeam("PRJ-01", "Hệ thống quản lý nhân sự")
    check(team.leader is None, "chưa có trưởng nhóm")
 
    print("\n6. addMember(employee)")
    check(team.add_member(emp2), "thêm E002")
 
    print("\n7. addMember(engineer, True) đặt làm trưởng nhóm")
    check(team.add_member(se2, True), "thêm S002 và đặt làm trưởng nhóm")
    check(team.leader is se2, "trưởng nhóm là S002")
 
    print("\n8. Thử thêm lại thành viên đã tồn tại")
    check(team.add_member(emp2) is False, "thêm lại E002 bị từ chối")
    check(team.size == 2, "kích thước nhóm vẫn là 2")
    team.add_member(se1)
 
    print("\n9. Hiển thị bằng lời gọi đa hình")
    team.display_team()
 
    print("\n10. Tổng chi phí nhân sự hằng tháng")
    expected = 13_000_000 + (22_000_000 + 3_000_000) + 0 + 0  # emp2 + se2 + se1 (lương 0)
    check(team.calculate_total_monthly_cost() == expected, f"tổng = {expected:,.0f}")
 
    print("\n11. Xóa trưởng nhóm hiện tại -> bị từ chối")
    check(team.remove_member("S002") is False, "không xóa được trưởng nhóm")
    check(team.contains("S002"), "S002 vẫn trong nhóm")
 
    print("\n12. Đổi trưởng nhóm rồi xóa trưởng nhóm cũ")
    check(team.change_leader(emp2), "đổi trưởng nhóm sang E002")
    check(team.remove_member("S002"), "xóa được S002 (trưởng nhóm cũ)")
    check(not team.contains("S002"), "S002 không còn trong nhóm 1")
    team.add_member(se2)  # đưa lại để phục vụ bước 13
    # trưởng nhóm mới chưa là thành viên -> tự được thêm
    newbie = Employee("E777", "Người mới", 5_000_000)
    check(team.change_leader(newbie) and team.contains("E777"), "trưởng nhóm mới tự được thêm vào nhóm")
    team.change_leader(emp2)
 
    print("\n13. Nhóm thứ hai chia sẻ nhân sự (kết tập nhiều nhóm)")
    print("\n14. Hủy nhóm 2 bằng khối lệnh cục bộ")
    local_block(emp2)
 
    print("\n15. Nhân sự của nhóm 2 vẫn tồn tại sau khi nhóm bị hủy")
    emp2.display_info()
    check(team.contains("E002"), "E002 vẫn thuộc nhóm 1")
    check(emp2.full_name == "Trần Thị B", "đối tượng E002 còn nguyên vẹn")
 
    test_edge_cases()
    print("\n=== Kết thúc chương trình (các đối tượng còn lại bị hủy) ===")
 
 
if __name__ == "__main__":
    main()