
import './App.css'
import Header from './components/Header'

import {
  QueryClient,
  QueryClientProvider,
  //useQuery,
} from '@tanstack/react-query'

import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";

import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import HomePage from './pages/HomePage';
import InitPage from './pages/data/InitPage';
import ViewPage from './pages/data/ViewPage';
import ChooseDataSetPage from './pages/pipeline/ChooseDataSetPage';
import UpdateDataSetPage from './pages/pipeline/UpdateDataSetPage';
import SelectPipelinePage from './pages/pipeline/SelectPipelinePage';
import CreatePipelinePage from './pages/pipeline/CreatePipelinePage';
import AnomaliesPage from './pages/data/AnomaliesPage';
import PipelineResultsPage from './pages/pipeline/PipelineResultsPage';

const queryClient = new QueryClient()

function App() {

  return (
    <>
    <QueryClientProvider client={queryClient}>
    <Router>
          <Header/>
          <Switch>
            <Route path="/login">
              <LoginPage />
            </Route>
            <Route path="/signup">
              <SignUpPage />
            </Route>
            <Route path="/data/initialisation">
              <InitPage />
            </Route>
            <Route path="/data/view">
              <ViewPage />
            </Route>
            <Route path="/data/anomalies">
              <AnomaliesPage />
            </Route>
            <Route path="/pipeline/data">
              <ChooseDataSetPage />
            </Route>
            <Route path="/pipeline/update">
              <UpdateDataSetPage />
            </Route>
            <Route path="/pipeline/select">
              <SelectPipelinePage />
            </Route>
            <Route path="/pipeline/create">
              <CreatePipelinePage />
            </Route>
            <Route path="/pipeline/results">
              <PipelineResultsPage />
            </Route>
            <Route path="/">
              <HomePage />
            </Route>
          </Switch>
    </Router>
    </QueryClientProvider>
      </>


  )
}

export default App

