import React, {Component} from 'react';

import "./TodoList.css";
import { getTodosTask } from "../../api/todos"

import "../../static/css/bootstrap.min.css";
//import "../../static/css/font-awesome/all.min.css";

//import GridLayout from 'react-grid-layout';
//import 'react-grid-layout/css/styles.css'
//import 'react-resizable/css/styles.css'

interface ITodo {
    id:             number
    task_name:      string
    task_desc:      string
    task_owner:     string
    create_date:    string
    last_modify_date: string
    is_complete:    boolean
}

class TodoList extends Component {
    state = {
        todos: [],
    }

    componentDidMount(): void {
        this.getTodosTask();
    }

        getTodosTask = () => {
            getTodosTask().then((response)=>{
                const todos = response.data.data;
                console.log(response.data.message);
                console.log(todos);
                this.setState({
                    todos: todos,
                });
            })
        }

    generateAddItemBtn = () => {
        return (
            <form className="">
                <div className="mb-3 input-group">
                    <input placeholder="New Item"
                           aria-describedby="basic-addon1"
                           type="text"
                           className="form-control"
                    />
                    <div className="input-group-append">
                        <button type="submit" className="btn btn-success">Add Item</button>
                    </div>
                </div>
            </form>
        )
    }

    generateDoneItemCalculator = () => {
        return (
            <div className="mb-3">
                <div className="done-group-calculator">
                    任务统计：已完成： {}  | 进行中：{}
                </div>
            </div>
        )
    }

    generateTodoList = () => {
        return (
            <div className="col-md-6">
                {this.generateAddItemBtn()}
                {this.generateTodoItems(this.state.todos, false)}
            </div>
        )
    }

    generateDoneList = () => {
        return (
            <div className="col-md-6">
                {this.generateDoneItemCalculator()}
                {this.generateTodoItems(this.state.todos, true)}
            </div>
        )
    }

        generateTodoItems = (itodos: ITodo[], is_complete: boolean) => {
        const div_classname = is_complete ? "item completed container-fluid" : 'item false container-fluid';
        const i_classname = is_complete ? "far fa-check-square" : 'far fa-square';
        const new_itodos = itodos.filter((itodo)=>{
            return itodo.is_complete == is_complete;
        });
        const todoitems = new_itodos.map((itodo)=>{
            return(
                <div className={div_classname} key={itodo.id}>
                    <div className="row">
                        <div className="text-center col-1">
                            <button aria-label="Mark item as complete" type="button"
                                    className="toggles btn btn-link btn-sm">
                                <i className={i_classname}></i>
                            </button>
                        </div>
                        <div className="name col-10">{itodo.task_name}</div>
                        <div className="text-center remove col-1">
                            <button aria-label="Remove Item" type="button" className="btn btn-link btn-sm">
                                <i className="fa fa-trash text-danger"></i>
                            </button>
                        </div>
                    </div>
                </div>
            )
        })
        return todoitems
        // const layout = [
        //                   {i: '1', x: 0, y: 0, w: 3, h: 2},
        //                   {i: '2', x: 0, y: 2, w: 3, h: 2},
        //                   {i: '3', x: 0, y: 4, w: 3, h: 2},
        //                   {i: '4', x: 0, y: 6, w: 3, h: 2},
        //                ];
        // const layouted_todoitems = <GridLayout
        //                                       className="layout"
        //                                       layout={layout}
        //                                       cols={12}
        //                                       rowHeight={30}
        //                                       width={1200}>
        //                                 {todoitems}
        //                            </GridLayout>;
        // return layouted_todoitems
    }

    render() {
        return (
            <div>
                Welcome to TodoList!
                <div className="container">
                    <div className="row">
                        {this.generateTodoList()}
                        {this.generateDoneList()}
                    </div>
                </div>
            </div>
        );
    }
}

export default TodoList;