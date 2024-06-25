import { Route, createBrowserRouter, createRoutesFromElements } from "react-router-dom";
import Home from "../screens/home";

const Router = createBrowserRouter(
    createRoutesFromElements(
        <Route>
            <Route path="/" element={<Home />} />
        </Route>
    )
)

export default Router;
