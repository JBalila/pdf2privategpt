const siteURL = 'http://localhost:5000/api/';

// Expects <route> to be without a leading '/' character
// Returns the API route depending on whether app is on localhost or production
export function buildPath(route: string): string {
    if (process.env.NODE_ENV === 'production')
        return siteURL + route;
    else
        return 'http://localhost:5000/api/' + route;
}