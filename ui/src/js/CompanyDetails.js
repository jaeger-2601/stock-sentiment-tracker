import { useParams } from 'react-router-dom';

function CompanyDetails () {
    const { companyTicker } = useParams();

    return (
        <h1> The company ticker is {companyTicker} </h1>
    )
}

export default CompanyDetails;