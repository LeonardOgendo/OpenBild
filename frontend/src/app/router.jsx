// Create router component

import { createBrowserRouter } from "react-router-dom";
import AppLayout from "./layout/AppLayout";
import HomePage from "../pages/HomePage";
import AuthPage from "../features/auth/AuthPage";
import Login from "../features/auth/components/Login";
import Signup from "../features/auth/components/Signup";

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />
  },
  {
    path: "/auth",
    element: <AuthPage />,
    children: [
        { path: 'login/', element: <Login /> },
        { path: 'register/', element: <Signup /> }
    ]
  },
  {
    path: '/dashboard',
    element: <AppLayout />,
  }  
]);

export default router;