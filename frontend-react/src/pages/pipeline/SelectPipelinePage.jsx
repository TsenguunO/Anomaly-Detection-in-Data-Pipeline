import { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { useAuthStore, usePipelineStore } from "../../stores";
import { Container, Row, Button, Col } from 'react-bootstrap';
import PipelineSideBar from '../../components/PipelineSidebar';
import axios from 'axios';
// import.meta.env.VITE_API_URL

const SelectPipelinePage = () => {
    const history = useHistory();
    const loggedInStatus = useAuthStore((state) => state.loggedInStatus);
    const loggedInUser = useAuthStore((state) => state.loggedInUser);
    if (!loggedInStatus) {
        history.push('/login');
    }

    const selectedDataset = usePipelineStore((state) => state.targetDataSetName);
    const selectedPipeline = usePipelineStore((state) => state.targetPipelineName);
    const setTargetPipelineName = usePipelineStore((state) => state.setTargetPipelineName);
    const [pipelines, setPipelines] = useState([]);

    //TODO: models remove after pipelines are implemented
    const [models, setModels] = useState([]);
    useEffect(() => {
        listModelsApi();
    }, []);
    const listModelsApi = async () => {
        const url = 'http://localhost:8000/api/model/get_all_models';
        const response = await fetch(url, {
          method: 'get',
          headers: {
            'Content-type': 'application/json',
          }
        });
        const data = await response.json();
        if (data.error) {
          alert(data.error)
        } else {
          setModels(data.model_list)
        }
      }


    useEffect(() => {
        listpipelinesApi();
    }, []);

    const listpipelinesApi = async () => {
        // event.preventDefault();
        const url = 'http://localhost:8000/api/pipeline/get_all_pipelines';
        const response = await fetch(url, {
          method: 'get',
          headers: {
            'Content-type': 'application/json',
          }
        });
        const data = await response.json();
        if (data.error) {
          // errorDialog
          alert(data.error)
        } else {
          // localStorage.setItem('token', data.token)
          // localStorage.setItem('email', email)
          // props.setToken(data.token);
          // navigate('/dashboard');
          // navigate('/');
          console.log(data.tables)
          setPipelines(data.pipeline_list)
        //   return 
        }
      }

    const getRunModelResult = () => {
        return axios.post(`${import.meta.env.VITE_API_URL}/api/anomalies/test_model__with_dataset`, {
            email: loggedInUser,
            model_name: selectedPipeline,
            model_version: 1,
            stored_tablename: selectedDataset,}
        );
    };

    const handleCreateButtonClick = () => {
        history.push('/pipeline/create');
    };

    const handleNextButtonClick = () => {
        const result = getRunModelResult();
        console.log(result);
        history.push('/pipeline/results');
    };

    const handleSelectModel = (model_name) => {
        setTargetPipelineName(model_name);
    };

    return (
        <Container fluid className="select-pipeline-page-container">
            <Row>
                <Col xs={2} id="sidebar-wrapper">
                    <PipelineSideBar />
                </Col>
                <Col xs={10} id="page-content-wrapper">
                    <Row className="justify-content-md-center text-center mt-4">
                        {/* <h1>Select a Pipeline to Run the Model</h1> */}
                        <h1>Select a Model to Run</h1>
                    </Row>
                    <Row className="justify-content-md-center text-center">
                        {/* <p>Existing pipelines for selected dataset:</p> */}
                        <p>Models:</p>
                    </Row>
                    <Row className="justify-content-md-center text-center">
                        {/* <Col md="auto">
                            <select 
                                value={selectedPipeline} 
                                onChange={(e) => setSelectedPipeline(e.target.value)}
                                className="mb-3"
                            >
                                <option value="">Select a pipeline</option>
                                {pipelines.map((pipeline, index) => (
                                    <option key={index} value={pipeline.pipeline_id}>
                                        {pipeline.pipeline_name}
                                    </option>
                                ))}
                            </select>
                        </Col> */}
                        <Col md="auto">
                            <select 
                                value={selectedPipeline} 
                                onChange={(e) => handleSelectModel(e.target.value)}
                                className="mb-3"
                            >
                                <option value="">Select a model</option>
                                {models.map((model, index) => (
                                    <option key={index} value={model.model_name}>
                                        {model.model_name}
                                    </option>
                                ))}
                            </select>
                        </Col>
                    </Row>
                    <Row className="justify-content-md-center">
                        <Col md="auto">
                            <Button onClick={handleCreateButtonClick} className="me-2">
                                Create new pipeline
                            </Button>
                            <Button onClick={handleNextButtonClick}>
                                Next
                            </Button>
                        </Col>
                    </Row>
                </Col>
            </Row>
        </Container>
    );
}

export default SelectPipelinePage;
