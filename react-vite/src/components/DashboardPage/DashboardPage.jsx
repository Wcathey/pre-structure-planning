import { NavLink } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import LoginForm from "../LoginForm";
import { createNewAssignment, getAllAssignments } from "../../redux/assignment";

function DashboardPage () {
  const dispatch = useDispatch();
  const user = useSelector((state) => state.session.user);
  useEffect(()=> {
    if(user) {
      dispatch(getAllAssignments())
    }
  }, [dispatch, user])



  return (
    <div className="dashboard-container">
      {user ?
      <div className="user-verified">

      </div> :
      <div className="login-container">
        <LoginForm/>
      </div>
    }

    </div>

    )


}

export default DashboardPage;
