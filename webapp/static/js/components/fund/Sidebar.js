import React from 'react'
import axios from 'axios'
import { saveAs } from 'file-saver'
import factsheets_logo from '../../../img/factsheets_logo.png'

class Sidebar extends React.Component {
  constructor() {
    super()

    this.state = {
      showManageData: false
    }

    this.handleClick = this.handleClick.bind(this)
    this.handleManageDataClick = this.handleManageDataClick.bind(this)
  }

  handleClick() {

    const data = {
      fund_name: this.props.fundName,
      fund_overview: this.props.fundOverview
    }

    axios.post('/api/fact_sheet', data)
      .then(response => {
        // download fact sheet
        const link = document.createElement('a')
        document.body.appendChild(link)
        link.style = 'display: none'
        link.href = '/api/download_fact_sheet'
        link.click()
        console.log('downloaded')
      })
  }

  handleManageDataClick() {
    console.log('hello from manage data click')
    this.setState({
      showManageData: this.state.showManageData ? false : true
    })
  }


  render() {
    const manageDataIsVisble = 
      this.state.showManageData ? 'visible' : 'hidden'

    console.log(manageDataIsVisble)

    return (
      <div className="sidebar">
        <div id="sidebar-logo">
          <img src={factsheets_logo} />
        </div>
        <ul>
          <div onClick={this.handleClick}>
            <li>Generate Report</li>
          </div>

          <div>
            <li
              onClick={this.handleManageDataClick}>
              Manage Data
            </li>
          </div>

          {/*<div
            className="sidebar-dropdown-item"
            id="manage-data-dropdown-items"
            ref="manage-data-dropdown-items"
            style={{visibility: manageDataIsVisble}}>
            <li>
              Fund Overview
            </li>
            <li>
              Monthly Returns
            </li>
          </div>*/}

          <div>
            <li>Report Components</li>
          </div>
        </ul>
      </div>
    )
  }
}

export default Sidebar