import React from 'react'
import axios from 'axios'
import { ReactTabulator } from 'react-tabulator'

import Sidebar from './Sidebar'
import Header from './Header'
import Modal from './Modal'

class Fund extends React.Component {

  constructor() {
    super()

    // get fundName from link
    let fundName = window.location.href
    fundName = fundName.split('/').slice(-1)[0]
    fundName = decodeURIComponent(fundName)

    // set initial state
    this.state = {
      fundName: fundName,
      returns: [],
      strategyAllocation: []
    }

    this.handleUpdateDataClick = this.handleUpdateDataClick.bind(this)
    this.handleChange = this.handleChange.bind(this)
  }

  componentDidMount() {
    axios.get('/api/fund', {
      params: {
        'fund_name': this.state.fundName
      }
    })
      .then((response) => {
        console.log(response.data)

        const strategyAllocation = response.data.strategy_allocation
        strategyAllocation.forEach((item, i) => {
          item.id = i
        })

        const returns = response.data.returns
        returns.forEach((item, i) => {
          item.id = i
        })

        this.setState({
          'fundOverview': response.data.fund_overview,
          'returns': returns,
          'strategyAllocation': strategyAllocation
        })
        console.log(this.state)
      })
  }

  handleUpdateDataClick() {
    // send axios request
    axios.put('/api/fund', {
      fund_name: this.state.fundName,
      fund_overview: this.state.fundOverview,
      returns: this.refs['returns-table'].props.data
    })
      .then((response) => {
        console.log('Updated fund')
        console.log(response)
      })
  }

  handleChange(event) {
    const { name, value, type, checked } = event.target
    type === 'checkbox' ? this.setState({ [name]: checked }) : this.setState({ [name]: value} )
  }

  render() {

    // define tabulator columns
    const returnsCols = [
      {title:"Year", field:"year"},
      {title:"Month", field:"month"},
      {title:"Return", field:"return", editor:true}
    ]

    const strategyAllocationCols = [
      {title:"Name", field:"name"},
      {title:"Dollars", field:"dollars", editor:true}
    ]

    return (
      <div id="body">
        <Sidebar 
          fundName={this.state.fundName}
          fundOverview={this.state.fundOverview} />

        <div className="container-fluid">

          <div className="content">
            <Header
              fundName={this.state.fundName} />
            <div>
              <label>Fund Overview</label>
              <div className="form-group">
                <textarea
                  className="form-control"
                  rows="5"
                  name="fundOverview"
                  value={this.state.fundOverview}
                  onChange={this.handleChange}>
                </textarea>
              </div>

              <div>
                <label>Fund Performance</label>
                <ReactTabulator 
                  ref='returns-table'
                  columns={returnsCols}
                  data={this.state.returns}
                  options={{'height': 200}} />
              </div>
              <br/>

              <div>
                <label>Strategy Allocation</label>
                <ReactTabulator 
                  ref='strategy-allocation-table'
                  columns={strategyAllocationCols}
                  data={this.state.strategyAllocation}
                  options={{'height': 130}} />
              </div>


              <hr/>
              <button
                className="btn btn-primary"
                onClick={ () => this.handleUpdateDataClick() }>
                Update Data
              </button>

              <button
                onClick={ () => console.log('clicked') }>
                Click me
              </button>

            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default Fund