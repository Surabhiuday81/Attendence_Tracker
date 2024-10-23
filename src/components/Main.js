import React, { useState } from "react";
import WebcamComponent from "./WebcamComponent";
import AttendanceStatus from "./AttendenceStatus";
import "./Main.css"; // Import the custom CSS file

const Main = () => {
  const [studentData, setStudentData] = useState(null);
  const [face, setFace] = useState(false);
  const [lesstime, setlesstime] = useState(false);

  const handleDataReceived = (data) => {
    setStudentData(data);
    setlesstime(false); // Reset lesstime when new data is received
  };

  const noface = (data) => {
    setFace(data);
  };

  const handlelesstime = (data) => {
    setlesstime(data);
  };

  return (
    <div className="d-flex flex-column align-items-center justify-content-center min-vh-100">
      <h1 className="text-center mb-5 headd">Attendance</h1>
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-6">
            <WebcamComponent
              onDataReceived={handleDataReceived}
              noface={noface}
              handlelesstime={handlelesstime}
            />
          </div>
          <div className="col-md-6">
            <AttendanceStatus
              key={studentData ? studentData.student_id : "default"} // Adding key
              studentData={studentData}
              face={face}
              lesstime={lesstime}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Main;
