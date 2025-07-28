import { Outlet } from "react-router-dom";

const AppLayout = () => {

    return (
        <div>
            <div>
                <h2>OpenCollab</h2>
                <Sidebar />
            </div>
            <div>
                <TopNav />
                <div className="main-content">
                    <Outlet />
                </div>
            </div>
        </div>
    )
}

export default AppLayout;