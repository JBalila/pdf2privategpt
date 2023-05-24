export default function QueryResponse({queryResponse}: {queryResponse: string}) {
    const queryResponseArr: string[] = queryResponse.split('\n');

    return(
        <div>
            {queryResponseArr.map(elem =>
                <div>
                    <p>{elem}</p>
                    <br />
                </div>
            )}
        </div>
    );
}