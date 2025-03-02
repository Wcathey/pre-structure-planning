const LOAD_ASSIGNMENTS = 'assignments/loadAssignments';
const LOAD_ASSIGNMENT_DETAILS = 'assignments/loadAssignmentDetails';
const LOAD_CURRENT_USER_ASSIGNEMNTS = 'assignments/loadCurrentUserAssignments';
const UPDATE_ASSIGNMENT = 'assignments/updateAssignment';
const CANCEL_ASSIGNMENT = 'assignments/cancelAssignment';
const CREATE_ASSIGNMENT = 'assignments/createAssignment';

const loadAssignments = (assignments) => ({
    type: LOAD_ASSIGNMENTS,
    assignments
});

const loadAssignmentDetails = (assignment) => ({
    type: LOAD_ASSIGNMENT_DETAILS,
    assignment
});

const updateAssignment = (assignment) => ({
    type: UPDATE_ASSIGNMENT,
    assignment
});

const cancelAssignment = (assignment) => ({
    type: CANCEL_ASSIGNMENT,
    assignment
});

const createAssignment = (assignment) => ({
    type: CREATE_ASSIGNMENT,
    assignment
});

const loadCurrentUserAssignments_Admin = (assignments) => ({
    type: LOAD_CURRENT_USER_ASSIGNEMNTS,
    assignments
});

export const getAllAssignments = () => async (dispatch) => {
    const response = await fetch("/api/assignments")
    if (response.ok) {
        const data = await response.json();
        dispatch(loadAssignments(data));
    } else if (response.status < 500) {
        const errorMessages = await response.json();
        return errorMessages
    } else {
        return { server: "Something went wrong. Please try again" }
    }
}

export const getAssignmentById = (id) => async (dispatch) => {
    const response = await fetch(`/api/assignments/${id}`)
    if (response.ok) {
        const data = await response.json();
        dispatch(loadAssignmentDetails(data));
        return data;
    } else if (response.status < 500) {
        const errorMessages = await response.json();
        return errorMessages
    } else {
        return { server: "Something went wrong. Please try again" }
    }
}

export const getUserAssignments = (id) => async (dispatch) => {
    const response = await fetch(`/api/assignments/user/${id}`)
    const data = await response.json();
    if (response.ok) {
        dispatch(loadCurrentUserAssignments_Admin(data));
        return response;

    } else if (response.status < 500) {
        const errorMessages = await response.json();
        return errorMessages
    } else {
        return { server: "Something went wrong. Please try again" }
    }
}

    export const updateAssignmentById = (assignment) => async (dispatch) => {
        const id = assignment.id
        const response = await fetch(`/api/assignments/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(assignment)
        });
        if (response.ok) {
            const data = await response.json();
            dispatch(updateAssignment(data));
            return data;
        } else if (response.status < 500) {
            const errorMessages = await response.json();
            return errorMessages
        } else {
            return { server: "Something went wrong. Please try again" }
        }
    }

    export const cancelAssignmentById = (assignment) => async (dispatch) => {
        const id = assignment.id
        const response = await fetch(`/api/assignments/${id}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(assignment)
        });
        if (response.ok) {
            const data = await response.json();
            dispatch(cancelAssignment(data));
            return data;
        } else if (response.status < 500) {
            const errorMessages = await response.json();
            return errorMessages
        } else {
            return { server: "Something went wrong. Please try again" }
        }

    }

    export const createNewAssignment = (assignment) => async (dispatch) => {
        const response = await fetch("/api/assignments", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(assignment)
        });
        if (response.ok) {
            const data = await response.json();
            dispatch(createAssignment(data));
            return data;
        } else if (response.status < 500) {
            const errorMessages = await response.json();
            return errorMessages
        } else {
            return { server: "Something went wrong. Please try again" }
        }

    }




    const initialState = {};

    function assignmentReducer(state = initialState, action) {
        switch (action.type) {
            case LOAD_ASSIGNMENTS: {
                const newState = { ...state, ...action }
                return newState;
            }
            case CREATE_ASSIGNMENT: {
                const newState = { ...state, ...action }
                return newState;
            }
            case LOAD_ASSIGNMENT_DETAILS: {
                const newState = { ...state, ...action }
                return newState;
            }
            case UPDATE_ASSIGNMENT: {
                const newState = { ...state, ...action }
                return newState;
            }
            case CANCEL_ASSIGNMENT: {
                const canceledAssignment = action.assignmentId
                const newState = { ...state, canceledAssignment }
                delete newState.canceledAssignment
                return newState
            }
            default:
                return state;
        }
    }

    export default assignmentReducer;
