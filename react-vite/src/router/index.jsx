import { createBrowserRouter } from 'react-router-dom';
import SignupFormPage from '../components/SignupFormPage';
import Layout from './Layout';
import DashboardPage from '../components/DashboardPage';


export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <DashboardPage/>,
      },
      {
        path: "signup",
        element: <SignupFormPage />,
      },

    ],
  },
]);
