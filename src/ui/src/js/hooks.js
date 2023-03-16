import { useState, useEffect } from "react";

function useFetch(url,  preprocessCallback=(data)=>data) {

    const [data, setData] = useState(null);

    useEffect( () => {

        const controller = new AbortController();

        fetch(url, { signal: controller.signal })
            .then((response) => response.json())
            .then((json_data) => {
                setData(preprocessCallback(json_data['data']));
            });
        
        return () => {
            console.log("fetch aborted!");
            controller.abort();
        };

    }, [url]);

    return [data, setData];
}

export default useFetch;