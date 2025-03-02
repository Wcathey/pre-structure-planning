import { NavLink } from "react-router-dom";
import { useState, useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import LoginForm from "../LoginForm";
import { createNewAssignment, getAllAssignments } from "../../redux/assignment";

function DashboardPage () {
  return (
    <>
    <h1>Dashboard</h1>
    </>
  )
}

export default DashboardPage;
