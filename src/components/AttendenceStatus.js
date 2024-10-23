import React, { useEffect } from "react";

const AttendanceStatus = ({ studentData, face, lesstime }) => {
  useEffect(() => {
    if (lesstime && studentData) {
      alert(`Try after some time in ${studentData.timetotake} seconds`);
    }
  }, [lesstime, studentData]);

  return (
    <div className="card">
      <div className="card-body card__content">
        <h5 className="card-title text-center">Attendance Status</h5>
        {face === false ? (
          <p>No familiar face detected</p>
        ) : (
          !lesstime &&
          studentData && (
            <div>
              <p>Student ID: {studentData.student_id}</p>
              <p>Name: {studentData.student_info.name}</p>
              <p>
                Total Attendance: {studentData.student_info.total_attendance}
              </p>
              <p>
                Last Attendance: {studentData.student_info.last_attendance_time}
              </p>
              <img src={studentData.img_url} alt="Student" />
            </div>
          )
        )}
      </div>
    </div>
  );
};

export default AttendanceStatus;
