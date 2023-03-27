import {Box, List, Pagination} from "@mui/material";
import ListItem from "@mui/material/ListItem";
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import LinkIcon from '@mui/icons-material/Link';
import React from "react";

const LinkList = ({pageData, onChangePage}) => (
    pageData.objects.length > 0 &&
    <Box sx={{width: '1', display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
        <List sx={{width: '100%', overflow: 'auto'}}>
            {pageData.objects.map((result) => (
                <ListItem key={`item-${result.id}`}>
                    <ListItemIcon>
                        <LinkIcon/>
                    </ListItemIcon>
                    <ListItemText primary={result.url}/>
                </ListItem>
            ))}
        </List>
        <Pagination count={Math.ceil(pageData.meta.total / pageData.meta.limit)} onChange={onChangePage}/>
    </Box>
)

export default LinkList;