// import DataTable from 'react-data-table-component'
import { GrDocumentUpdate } from "react-icons/gr";
import { MdOutlineMonetizationOn } from "react-icons/md";
import {useDispatch , useSelector} from "react-redux";
import { useEffect, useState } from 'react';
import {Menu,Search_input} from '../index'
import {getAll} from '../../Redux/API/GetAll'
const Client = () => {

    const [Search, setSearch] = useState("");

    const dispatch = useDispatch();
    const Clients = useSelector(state => state.ClientList.ClientsList);
    const isLoading = useSelector(state => state.ClientList.isLoading)

    useEffect(()=>{
        // dispatch(getAll("http://127.0.0.1:8000/api/clients"));
        dispatch(getAll("https://jsonplaceholder.typicode.com/users"));
    },[dispatch]);
    return (
        <>
        <Menu/>

            <div>
                <h1 className="text-[--statistic-color] text-3xl m-4">Client</h1>
                <Search_input
                    onChange={(e) => setSearch(e.target.value)}
                />

                <button className='text-xs  py-1 px-2 border-none ml-1 rounded-md bg-[--statistic-color] my-3 ml-[630px]  hover:bg-[--light-color]'>
                    <a href="/AddClient" className='font-semibold'>Ajouter +</a>
                </button>

                <table className="ml-5 ">
                    <thead className=' w-80  text-sm  bg-[--statistic-color] text-white font-semibold'>
                        <tr className="m-2">
                            <th scope="col" className='py-2 px-4'>id</th>
                            <th scope="col" className='py-2 px-4'>Code</th>
                            <th scope="col" className='py-2 px-4'>Nom</th>
                            <th scope="col" className='py-2 px-4'>Email</th>
                            <th scope="col" className='py-2 px-4'>Address</th>
                            <th scope="col" className='py-2 px-4'>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            isLoading ?
                                <div class="d-flex align-items-center text-primary">
                                    <strong>Loading...</strong>
                                    <div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>
                                </div>:
                                Clients
                                    .filter((client) => {
                                        return Search.toLowerCase() === ''
                                            ? client
                                            : client.name.toLowerCase().includes(Search)
                                    })
                                    .map((client) => (
                                        <tr key={client.id} className="text-xs shadow-md">
                                            <td className="pl-6">{client.id}</td>
                                            <td className="p-3 ">{client.name}</td>
                                            <td>{client.username}</td>
                                            <td>{client.email}</td>
                                            <td>{client.website}</td>
                                            <td>
                                                <button to={`/edit/${client.id}`} className='border-none ml-1 px-1 py-1 bg-[--statistic-color]'><a href="/Update"><GrDocumentUpdate  /></a></button>
                                                <button className='border-none ml-1 px-1 py-1 bg-[--statistic-color]'><a href="#"><MdOutlineMonetizationOn /></a></button>
                                            </td>
                                        </tr>
                                    ))
                        }
                    </tbody>
                </table>
            </div>

        </>
    )
}

export default Client