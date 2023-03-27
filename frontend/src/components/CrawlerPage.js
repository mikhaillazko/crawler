import React, {useState} from 'react';
import {Backdrop, Box, Button, CircularProgress, Container, TextField} from "@mui/material";
import useInterval from "use-interval";
import {addTask, getTask, getTaskResults} from "../api";
import LinkList from "./LinkList";

const taskStatusCompleted = "completed";

const CrawlerPage = () => {
    const [siteUrl, setSiteUrl] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [task, setTask] = useState(null);
    const [delay, setDelay] = useState(null);
    const [linkPage, setLinkPage] = useState({objects: [], meta: {total: 0, offset: 0}});
    const [isLoading, setIsLoading] = useState(false);

    const handleAddTask = async () => {
        setIsLoading(true);
        try {
            const response = await addTask(siteUrl)
            setTask(response.data);
            setDelay(2000)
        } catch (e) {
            setIsLoading(false)
            setErrorMessage(e.response.data?.detail[0]?.msg)
        }
    }

    const handleChangePage = async (event, value) => {
        const resultResponse = await getTaskResults(task.id, (value - 1) * linkPage.meta.limit);
        setLinkPage(resultResponse.data);
    }

    useInterval(async () => {
        const taskResponse = await getTask(task.id)
        if (taskResponse.data.status === taskStatusCompleted) {
            setDelay(null)
            setTask(taskResponse.data);
            const resultResponse = await getTaskResults(task.id, linkPage.meta.offset);
            setLinkPage(resultResponse.data);
            setIsLoading(false);
        }
    }, delay);

    return (
        <Container
            sx={{
                padding: '50px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                width: '100%',
            }}
        >
            <Box>
                <TextField
                    variant="standard"
                    value={siteUrl}
                    onChange={(e) => setSiteUrl(e.target.value)}
                    error={!!errorMessage}
                    helperText={errorMessage}
                    sx={{marginRight: '1rem', width: 400}}
                    placeholder='Enter site url'
                />
                <Button variant="contained" onClick={handleAddTask}>Go</Button>
            </Box>
            <LinkList pageData={linkPage} onChangePage={handleChangePage}/>
            <Backdrop sx={{color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1}} open={isLoading}>
                <CircularProgress color="inherit"/>
            </Backdrop>
        </Container>
    );
}

export default CrawlerPage