import { useState, useEffect } from "react";
import { thunkLogin, getDemoUserData } from "../../redux/session";
import { useDispatch, useSelector } from "react-redux";
import { NavLink } from "react-router-dom";
import "./LoginForm.css";

function LoginForm() {
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [selectedDemo, setSelectedDemo] = useState(""); // Track selected demo user
  const [errors, setErrors] = useState({});

  useEffect(() => {
    dispatch(getDemoUserData());
  }, [dispatch]);

  const demoUsers = useSelector((state) => state.session.users);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const serverResponse = await dispatch(
      thunkLogin({
        email,
        password,
      })
    );

    if (serverResponse) {
      setErrors(serverResponse);
    }
  };

  const handleDemoSelect = (e) => {
    const selectedEmail = e.target.value;
    setSelectedDemo(selectedEmail); // Update selected option
    if (selectedEmail) {
      setEmail(selectedEmail);
      setPassword("password"); // Assuming all demo accounts use "password"
    }
  };

  const handleClear = () => {
    setEmail("");
    setPassword("");
    setSelectedDemo(""); // Reset the select dropdown
  };

  return (
    <>
      <h1>Log In</h1>

      <form onSubmit={handleSubmit}>
        <label>
          Email
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>
        {errors.email && <p>{errors.email}</p>}

        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>
        {errors.password && <p>{errors.password}</p>}

        <button type="submit">Log In</button>
        <button type="button" onClick={handleClear}>Clear</button>

        {demoUsers && (
          <select name="demo" id="demo-map" value={selectedDemo} onChange={handleDemoSelect}>
            <option value="">Select a Demo User</option>
            {demoUsers.accounts.map((demo) => (
              <option key={demo.id} value={demo.email}>
                {demo.username}
              </option>
            ))}
          </select>
        )}

        <p>Don't have an account? Signup Today!</p>
        <NavLink to="/signup">Signup</NavLink>
      </form>
    </>
  );
}

export default LoginForm;
