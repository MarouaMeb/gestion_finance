import { FaDownload } from "react-icons/fa";
import { FaFilePdf } from "react-icons/fa6";
import { IoMdInformationCircleOutline } from "react-icons/io";
import { GrDocumentUpdate } from "react-icons/gr";
import {useDispatch , useSelector} from "react-redux";
import { useEffect, useState } from 'react';
import {Menu,Search_input} from '../index'
import {getAll} from '../../Redux/API/GetAll'
const Facture_service = () => {

    const [Search, setSearch] = useState("");

    const dispatch = useDispatch();
    const Clients = useSelector(state => state.ClientList.ClientsList);
    const isLoading = useSelector(state => state.ClientList.isLoading)


    useEffect(()=>{
        dispatch(getAll("https://jsonplaceholder.typicode.com/users"));
    },[dispatch]);
    return (
        <>
        <Menu/>

            <div>
                <h1 className="text-[--statistic-color] text-3xl m-4">Facture service</h1>
                <Search_input
                    onChange={(e) => setSearch(e.target.value)}
                />

                <button className='text-xs  py-1 px-2 border-none ml-1 rounded-md bg-[--statistic-color] my-3 ml-[630px]  hover:bg-[--light-color] hover:text-[--statistic-color]'>
                    <a href="/AddFacturService" className='font-semibold'>Ajouter +</a>
                </button>

                <table className="ml-5 ">
                    <thead className=' w-80  text-sm  bg-[--statistic-color] text-white font-semibold'>
                        <tr className="m-2">
                            <th scope="col" className='py-2 px-4'>id</th>
                            <th scope="col" className='py-2 px-4'>Code client</th>
                            <th scope="col" className='py-2 px-4'>Nom client</th>
                            <th scope="col" className='py-2 px-4'>Numero de facture</th>
                            <th scope="col" className='py-2 px-4'>Date de creation</th>
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
                                : client.title.toLowerCase().includes(Search)
                        })
                        .map((client) => (
                            <tr key={client.id} className="text-xs shadow-md">
                                <td className="pl-6">{client.id}</td>
                                <td className="p-3 ">{client.username}</td>
                                <td>{client.name}</td>
                                <td>{client.email}</td>
                                <td>{client.website}</td>
                                <td>
                                    <button className='border-none ml-1 px-1 py-1 bg-[--statistic-color]'><a href="#"><IoMdInformationCircleOutline /></a></button>
                                    <button className='border-none ml-1 px-1 py-1 bg-[--statistic-color]'><a href="/Update"><FaDownload /></a></button>
                                    <button className='border-none ml-1 px-1 py-1 bg-[--statistic-color]'><a href="#"><FaFilePdf /></a></button>
                                    <button className='border-none ml-1 px-1 py-1 bg-[--statistic-color]'><a href="#"><GrDocumentUpdate /></a></button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

        </>
    )
}

export default Facture_service