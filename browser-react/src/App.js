import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Browser from "./Browser.js";

function App() {
  return (
    <Router>
      <div>
        {/* A <Switch> looks through its children <Route>s and
        renders the first one that matches the current URL. */}
        <Switch>
          <Route path="/browser/:path" component={getBrowser}></Route>
          <Route path="/">
            <Browser />
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

function Home() {
  return <h2>Home</h2>;
}

function getBrowser(props) {
  console.log(window.location.pathname);
  return <Browser path={window.location.pathname}></Browser>;
}

export default App;
