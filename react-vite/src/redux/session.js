const SET_USER = 'session/setUser';
const REMOVE_USER = 'session/removeUser';
const LOAD_DEMO_USERS = 'session/loadDemoUsers';

const setUser = (user) => ({
  type: SET_USER,
  payload: user
});

const removeUser = () => ({
  type: REMOVE_USER
});

const loadDemoUsers = (users) => ({
  type: LOAD_DEMO_USERS,
  payload: users
})

export const thunkAuthenticate = () => async (dispatch) => {
  const response = await fetch("/api/auth/");
  if (response.ok) {
    const data = await response.json();
    if (data.errors) {
      return;
    }

    dispatch(setUser(data));
  }
};

export const thunkLogin = (credentials) => async dispatch => {
  const response = await fetch("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials)
  });

  if (response.ok) {
    const data = await response.json();
    dispatch(setUser(data));
  } else if (response.status < 500) {
    const errorMessages = await response.json();
    return errorMessages
  } else {
    return { server: "Something went wrong. Please try again" }
  }
};

export const thunkSignup = (user) => async (dispatch) => {
  const response = await fetch("/api/auth/signup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(user)
  });

  if (response.ok) {
    const data = await response.json();
    dispatch(setUser(data));
  } else if (response.status < 500) {
    const errorMessages = await response.json();
    return errorMessages
  } else {
    return { server: "Something went wrong. Please try again" }
  }
};

export const thunkLogout = () => async (dispatch) => {
  await fetch("/api/auth/logout");
  dispatch(removeUser());
};

export const getDemoUserData = () => async (dispatch) => {
  const response = await fetch("/api/users/demo");
  if (response.ok) {
    const data = await response.json();
    dispatch(loadDemoUsers(data));
  } else if (response.status < 500) {
    const errorMessages = await response.json();
    return errorMessages;
  } else {
    return { server: "Something went wrong. Please try again" }
  }

}

const initialState = { user: null };

function sessionReducer(state = initialState, action) {
  switch (action.type) {
    case SET_USER: {
      const newState = { ...state, user: action.payload };
      return newState;
    }
    case REMOVE_USER: {
      const newState = { ...state, user: null };
      return newState;
    }
    case LOAD_DEMO_USERS: {
      const newState = { ...state, users: action.payload }
      return newState;
    }
    default: return state;

  }

}

export default sessionReducer;
