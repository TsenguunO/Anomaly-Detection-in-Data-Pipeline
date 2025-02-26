import { Button, Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';

function PipelineSideBar() {
  return (
    <Nav className="flex-column" style={{ 
        paddingTop: '76px', 
        backgroundColor: '#82ADDC',
        height: '100vh',
        position: 'fixed',
        top: 0,
        left: 0,
        width: '150px'
      }}>
      <Link to="/pipeline/data" style={{ width: '100%' }}>
        <Button style={{ 
          width: '100%', 
          backgroundColor: '#FFFFFF', 
          borderColor: '#005BC5', 
          color: 'black', 
          padding: '10px 0', 
          textAlign: 'center',
          borderBottom: '1px solid #00BFFF',
        }}>
          <div><img src="/viewdata.png" alt="View Data" style={{ marginBottom: '5px', width: '25px', height: '25px' }} /></div>
          <div>Pipeline Data</div>
        </Button>
      </Link>
      <Link to="/pipeline/select" style={{ width: '100%' }}>
        <Button style={{ 
          width: '100%', 
          backgroundColor: '#FFFFFF', 
          borderColor: '#005BC5', 
          color: 'black', 
          padding: '10px 0', 
          textAlign: 'center',
          borderBottom: '1px solid #00BFFF',
        }}>
          <div><img src="/selectpipeline.png" alt="Select Pipeline" style={{ marginBottom: '5px', width: '25px', height: '25px' }} /></div>
          <div>Select Pipeline</div>
        </Button>
      </Link>
      <Link to="/pipeline/results" style={{ width: '100%' }}>
        <Button style={{ 
          width: '100%', 
          backgroundColor: '#FFFFFF', 
          borderColor: '#005BC5', 
          color: 'black', 
          padding: '10px 0', 
          textAlign: 'center',
          borderBottom: '2px solid #00BFFF',
        }}>
          <div><img src="/anomalies.png" alt="Pipeline Results" style={{ marginBottom: '5px', width: '25px', height: '25px' }} /></div>
          <div>Pipeline Results</div>
        </Button>
      </Link>
    </Nav>
  );
}

export default PipelineSideBar;
