import pandas as pd
import streamlit as st
from database import add_student, get_student, get_students
from services import calculate_grade, calculate_statistics

# Səhifə konfiqurasiyası
st.set_page_config(
    page_title="Student Performance Dashboard", page_icon="🎓", layout="wide"
)

# Tamamilə Yeni və Fərqli Müasir Dizayn (Custom CSS)
st.markdown(
    """
    <style>
        .main {
            background-color: #fafbfc;
            padding: 2rem;
        }
        /* Unikal Başlıq Banneri */
        .dashboard-header {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 25px;
            border-radius: 16px;
            color: white;
            margin-bottom: 25px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
        }
        .dashboard-header h1 {
            color: white !important;
            margin-bottom: 5px;
        }
        .dashboard-header p {
            color: #94a3b8;
            margin: 0;
            font-size: 1.1rem;
        }
        /* Metrik Kartları */
        .stMetric {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        }
        /* Form Konteyneri */
        div[data-testid="stForm"] {
            background-color: #ffffff;
            border-radius: 14px;
            padding: 24px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def display_students(students):
  """Tələbələrin siyahısını və qiymət dərəcələrini göstərir."""

  if not students:
    st.info("Hələ heç bir tələbə əlavə edilməyib.")
    return

  for student in students:
    student["Grade"] = calculate_grade(student["Score"])

  dataframe = pd.DataFrame(students)
  dataframe = dataframe.rename(
      columns={
          "StudentID": "ID",
          "Name": "Name",
          "Score": "Score",
          "Grade": "Grade",
      }
  )

  st.dataframe(
      dataframe[["ID", "Name", "Score", "Grade"]],
      use_container_width=True,
      hide_index=True,
  )


def display_statistics(students):
  """Tələbələrin ümumi statistikasını göstərir."""

  statistics = calculate_statistics(students)

  col1, col2, col3, col4 = st.columns(4)

  col1.metric("Total Students", statistics["total_students"])
  col2.metric("Average Score", statistics["average_score"])
  col3.metric("Highest Score", statistics["highest_score"])
  col4.metric("Lowest Score", statistics["lowest_score"])


def main():
  # Unikal Başlıq Banneri
  st.markdown(
      """
        <div class="dashboard-header">
            <h1>🎓 Student Performance Dashboard</h1>
            <p>Tələbə nəticələrinin idarə edilməsi və analitika sistemi</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  try:
    students = get_students()

    # İki sütunlu struktur: Sol tərəfdə Əlavə et və Axtar, Sağ tərəfdə Statistika və Cədvəl
    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
      # Tələbə əlavə etmək
      st.header("Add Student")

      with st.form("add_student_form"):
        student_name = st.text_input("Student Name")

        score = st.number_input(
            "Score", min_value=0, max_value=100, value=0, step=1
        )

        submitted = st.form_submit_button(
            "Add Student", use_container_width=True
        )

        if submitted:
          if not student_name.strip():
            st.error("Tələbənin adını daxil edin!")
          else:
            try:
              add_student(student_name.strip(), int(score))
              st.success("Tələbə uğurla əlavə edildi!")
              st.rerun()
            except Exception as error:
              st.error(f"Tələbə əlavə edilə bilmədi: {error}")

      st.markdown("<br>", unsafe_allow_html=True)

      # Tələbə axtarışı
      st.header("Search Student")

      search_name = st.text_input(
          "Tələbənin adını daxil edin", key="search_student"
      )

    with col_right:
      # Statistikalar
      st.header("Statistics")
      display_statistics(students)

      st.divider()

      # Tələbələrin siyahısı
      st.header("Student List")
      if search_name.strip():
        matching_students = get_student(search_name.strip())

        if matching_students:
          display_students(matching_students)
        else:
          st.warning("Tələbə tapılmadı.")
      else:
        display_students(students)

  except Exception as error:
    st.error(f"Database ilə işləyərkən xəta baş verdi: {error}")


if __name__ == "__main__":
  main()