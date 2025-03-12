from sqlalchemy.orm import Session
from database import *
from model  import Sessions, Students, Volunteers, WrittenExamScores, VivaTranscripts, PracticalExamReports
from datetime import date, time
from alembic.config import Config
from alembic import command

def get_existing_sessions(db: Session):
    sessions = db.query(Sessions).all()
    while True:
        print("\nAvailable Sessions:")
        print("choose from the following session IDs:")
        for session in sessions:
            print(f"- ID: {session.id}")
        new_session = int(input("Enter your session ID: "))
        if new_session in [s.id for s in sessions]:
            return new_session
        else:
            print("Invalid session try again")

def get_existing_students(db: Session):
    students = db.query(Students).all()
    while True:
        print("\nAvailable Students:")
        print("choose from the following student IDs:")
        for student in students:
            print(f"- ID: {student.id}")
        new_student = int(input("Enter your student ID: "))
        if new_student in [s.id for s in students]:
            return new_student
        else:
            print("Invalid student try again")

def get_existing_volunteers(db: Session):
    volunteers = db.query(Volunteers).all()
    while True:
        print("\nAvailable volunteers:")
        print("choose from the following volunteer IDs:")
        for volunteer in volunteers:
            print(f"ID: {volunteer.id}")
        new_volunteer = int(input("Enter your volunteer ID: "))
        if new_volunteer in [v.id for v in volunteers]:
            return new_volunteer
        else:
            print("Invalid volunteer try again")


def insert_sessions(db: Session):
    id = int(input("Enter session id: "))
    name = input("Enter session name: ")
    total_classes=int(input("Enter total session classes: "))
    school_name = input("Enter school name: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    new_session = Sessions(
        id = id,
        name=name,
        total_classes=total_classes,
        school_name=school_name,
        start_date=date.fromisoformat(start_date),
        end_date=date.fromisoformat(end_date)
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


def insert_students(db: Session):
    id = int(input("Enter student id: "))
    first_name = input("Enter student's first name: ")
    mid_name = input("Enter student's mid name: ")
    last_name = input("Enter student's last name: ")
    age = int(input("Enter student's age: "))
    date_of_birth = input("Enter student's date of birth (YYYY-MM-DD): ")
    gender = input("Enter student's gender: ")
    classes_attended = int(input("Enter student's attendance: "))


    new_student = Students(
        id = id,
        first_name=first_name,
        mid_name=mid_name,
        last_name=last_name,
        age=age,
        date_of_birth=date.fromisoformat(date_of_birth),
        gender=gender,
        classes_attended=classes_attended,  # Default to 0 or get from user
        session_id=get_existing_sessions(db)
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


def insert_volunteers(db: Session):
    id = int(input("Enter volunteer id: "))
    first_name = input("Enter volunteer's first name: ")
    mid_name = input("Enter volunteer's mid name: ")
    last_name = input("Enter volunteer's last name: ")
    age = input("Enter volunteer's age: ")
    date_of_birth=input("Enter volunteer's date of birth (YYYY-MM-DD): ")
    gender=input("Enter volunteer's gender: ")
    email = input("Enter volunteer's email: ")
    phone_number = input("Enter volunteer's phone number: ")
    previous_ngo_experience=input("Enter volunteer's previous ngo experience: ")
    city = input("Enter volunteer's city: ")
    address = input("Enter volunteer's address: ")
    occupation = input("Enter volunteer's occupation: ")
    institute = input("Enter volunteer's institution: ")
    cv_link= input("Enter volunteer's cv link: ")
    insta_id= input("Enter volunteer's insta id: ")
    linked_in = input("Enter volunteer's linked_in: ")
    has_discord = bool(input("Does volunteer has a discord(True/False): "))
    classes_attended=int(input("Enter volunteer's attended classes: "))
    ses_id=get_existing_sessions(db)
    ses_name=db.query(Sessions.name).filter(Sessions.id == ses_id).scalar()


    new_volunteer = Volunteers(
        id=id,
        session_id=ses_id,
        session_name = ses_name,
        first_name=first_name,
        mid_name=mid_name,
        last_name=last_name,
        age = age,
        date_of_birth = date_of_birth,
        gender = gender,
        email=email,
        phone_number=phone_number,
        previous_ngo_experience=previous_ngo_experience,
        city=city,
        address=address,
        occupation=occupation,
        institute=institute,
        cv_link=cv_link,
        insta_id=insta_id,
        linked_in=linked_in,
        has_discord=has_discord,
        classes_attended=classes_attended  # Default to 0 or get from user
    )
    db.add(new_volunteer)
    db.commit()
    db.refresh(new_volunteer)
    return new_volunteer


def insert_written_exam_scores(db: Session):
    id= int(input("Enter written exam id: "))
    exam_type = input("Enter exam type: ")
    exam_date = input("Enter exam date (YYYY-MM-DD): ")
    written_ai_score = float(input("Enter AI section score: "))
    written_env_score = float(input("Enter Environment section score: "))
    written_internet_score = float(input("Enter Internet section score: "))
    written_canva_score = float(input("Enter Canva section score: "))
    written_programming_score = float(input("Enter Programming section score: "))
    written_hardware_software_score = float(input("Enter Hardware/Software section score: "))
    other_new_section_score_aggregated = float(input("Enter New section score: "))
    total_student_marks=float(input("Enter Student gained marks: "))
    total_marks_of_exam=float(input("Enter Total marks: "))
    start_time_exam=input("Enter exam start time (HH-MM): ")
    end_time_exam=input("Enter exam end time (HH-MM): ")
    stu_id = get_existing_students(db)
    stu_ses = db.query(Students.session_id).filter(Students.id == stu_id).scalar()

    new_score = WrittenExamScores(
        id =id,
        exam_type=exam_type,
        exam_date=date.fromisoformat(exam_date),
        written_ai_section_score=written_ai_score,
        written_env_score=written_env_score,
        written_internet_score=written_internet_score,
        written_canva_score=written_canva_score,
        written_programming_score=written_programming_score,
        written_hardware_software_score=written_hardware_software_score,
        other_new_section_score_aggregated=other_new_section_score_aggregated,
        total_student_marks=total_student_marks,
        total_marks_of_exam=total_marks_of_exam,
        start_time_exam=time.fromisoformat(start_time_exam),
        end_time_exam=time.fromisoformat(end_time_exam),
        student_id=stu_id,
        session_id=stu_ses
    )
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return new_score


def insert_viva_transcripts(db: Session):
    id = int(input("Enter viva id: "))
    exam_type=input("Enter exam type: ")
    exam_date=input("Enter exam date (YYYY-MM-DD): ")
    transcript=input("Enter viva transcript: ")
    stu_id = get_existing_students(db)
    stu_ses = db.query(Students.session_id).filter(Students.id == stu_id).scalar()
    vol_id = get_existing_volunteers(db)

    new_viva = VivaTranscripts(
            id = id,
            student_id=stu_id,
            volunteer_id=vol_id,
            exam_type=exam_type,
            exam_date=date.fromisoformat(exam_date),
            transcript=transcript,
            session_id=stu_ses
    )
    db.add(new_viva)
    db.commit()
    db.refresh(new_viva)
    return new_viva


def insert_practical_exam_report(db: Session):
    id = int(input("Enter practical id: "))
    exam_type= input("Enter exam type: ")
    exam_date=input("Enter exam date (YYYY-MM-DD): ")
    report=input("Enter practical report: ")
    stu_id = get_existing_students(db)
    stu_ses = db.query(Students.session_id).filter(Students.id == stu_id).scalar()
    vol_id = get_existing_volunteers(db)

    new_practical = PracticalExamReports(
        id = id,
        student_id=stu_id,
        session_id=stu_ses,
        volunteer_id=vol_id,
        exam_type=exam_type,
        exam_date=date.fromisoformat(exam_date),
        report=report
    )
    db.add(new_practical)
    db.commit()
    db.refresh(new_practical)
    return new_practical



def create_tables():
    from model import Base
    Base.metadata.create_all(bind=engine)

def main():
    create_tables()  # Ensure tables are created
    db = SessionLocal()
    try:
        while True:
            print("\nSelect an option out of following:")
            print("1. Insertion to DB")
            print("2. Updating DB")
            print("3. Exit")
            option = int(input("Enter the corresponding index: "))
            if option == 1:
                print("\nSelect an option to insert data:")
                print("1. Insert Session")
                print("2. Insert Student")
                print("3. Insert Volunteer")
                print("4. Insert Written Exam Scores")
                print("5. Insert Viva TRanscript")
                print("6. Insert Practical Exam Report")
                print("7. Exit")
                choice1 = int(input("Enter choice: "))
                if choice1 == 1:
                    insert_sessions(db)
                elif choice1 == 2:
                    insert_students(db)
                elif choice1 == 3:
                    insert_volunteers(db)
                elif choice1 == 4:
                    insert_written_exam_scores(db)
                elif choice1 == 5:
                    insert_viva_transcripts(db)
                elif choice1 == 6:
                    insert_practical_exam_report(db)
                elif choice1 == 7:
                    print("Exiting...")
                    print("Changes made to Database!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            elif option==2:
                print("\nSelect an option to update data:")
                print("1. Changing Column type for volunteer")
                print("2. Delete mid name from students")
                print("3. Added new column to students")
                print("4. Exit")
                choice2= int(input("Enter choice: "))
                if choice2==1:
                    alembic_cfg = Config("alembic.ini")
                    command.upgrade(alembic_cfg, "9d4b136d938e")
                elif choice2==2:
                    alembic_cfg = Config("alembic.ini")
                    command.upgrade(alembic_cfg, "06d502559373")
                elif choice2==3:
                    alembic_cfg = Config("alembic.ini")
                    command.upgrade(alembic_cfg, "6bd1d0f94e53")
                elif choice2 == 4:
                    print("Exiting...")
                    print("Changes made to Database!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            elif option == 3:
                print("Exiting...")
                print("Changes made to Database!")
                break
            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()