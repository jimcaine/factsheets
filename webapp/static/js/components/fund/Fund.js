import React from 'react'
import axios from 'axios'
import { ReactTabulator } from 'react-tabulator'

import Sidebar from './Sidebar'
import Header from './Header'

class Fund extends React.Component {

  constructor() {
    super()

    // get fundName from link
    let fundName = window.location.href
    fundName = fundName.split('/').slice(-1)[0]
    fundName = decodeURIComponent(fundName)

    // set initial state
    this.state = {
      fundName: fundName
    }

    this.handleClick = this.handleClick.bind(this)
    this.handleChange = this.handleChange.bind(this)
  }

  componentDidMount() {
    axios.get('/api/fund', {
      params: {
        'fund_name': this.state.fundName
      }
    })
      .then((response) => {
        this.setState({
          'fundOverview': response.data.fund_overview
        })
      })
  }

  handleClick() {
    axios.put('/api/fund', {
      fund_name: this.state.fundName,
      fund_overview: this.state.fundOverview
    })
      .then((response) => {
        console.log('Updated data:')
        console.log(response)
      })
  }

  handleChange(event) {
    const { name, value, type, checked } = event.target
    type === 'checkbox' ? this.setState({ [name]: checked }) : this.setState({ [name]: value} )
  }

  render() {

    // define tabulator data
    const columns = [
      {title:"Year", field:"year"},
      {title:"Month", field:"month"},
      {title:"Return", field:"return", editor:true}
    ]

    const data = [
      {"id": 0, "month": "January", "year": 2019, "return": 10.5}
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
                  columns={columns}
                  data={data} />
              </div>
              <br/>

              <button
                className="btn btn-primary"
                onClick={ () => this.handleClick() }>
                Update Data
              </button>

            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default Fund