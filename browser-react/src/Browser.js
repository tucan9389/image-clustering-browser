import React, { Component } from "react";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import { Table, Container, Header } from "semantic-ui-react";
import GridGallery from "./GridGallery";
import PaginationExampleCustomization from "./PaginationExampleCustomization";

const axios = require("axios");

class Browser extends Component {
  state = { clu_names: [], page: 1 };

  constructor(props) {
    super(props);

    this.setState({ target_path: "", clu_names: [], photos: [] });
    this.update();
  }

  componentDidUpdate(prevProps) {
    if (prevProps.path !== this.props.path) {
      this.update();
    }
  }

  getPath() {
    return window.location.pathname == "/browser"
      ? "/browser/"
      : window.location.pathname;
  }

  update() {
    var queryDict = {};
    var pathname = this.getPath();
    window.location.search
      .substr(1)
      .split("&")
      .forEach(function (item) {
        queryDict[item.split("=")[0]] = item.split("=")[1];
      });
    // console.log(queryDict);
    this.updatePath(pathname, queryDict.page ? parseInt(queryDict.page) : 1);
  }

  updatePath(path, page) {
    // console.log(page);
    var target_path = path;
    if (!target_path) {
      target_path = "/";
    }
    target_path = target_path.replace("/browser", "");

    const request_path =
      "http://0.0.0.0:8001" + "/browse" + target_path + "?page=" + page;
    // console.log(request_path);

    axios.get(request_path).then((response) => {
      // handle success
      const clu_names = response.data.clu_names;
      const img_names = response.data.img_names;
      const photos = img_names.map((img_name) => {
        return { src: "http://0.0.0.0:8001/" + img_name };
      });
      const totalPages = response.data.total_pages;
      const totalImages = response.data.total_images;
      // console.log(clu_names);
      // console.log(photos);
      this.setState({
        clu_names,
        target_path,
        photos,
        page,
        totalPages,
        totalImages,
      });
    });
  }

  handlePaginationChange = (activePage) => {
    // history.push("/path?page" + activePage);
    const onlyPath = this.getPath().split("?")[0];
    window.location.href = onlyPath + "?page=" + activePage;
    // console.log("activePage:" + activePage);
    this.setState({ page: activePage });
    // this.props.handlePaginationChange(activePage);
  };

  render() {
    const {
      clu_names,
      target_path,
      photos,
      page,
      totalPages,
      totalImages,
    } = this.state;
    const rootPath = "/browser" + target_path;
    var dirs = ("/browser" + target_path).split("/");
    dirs.pop();
    const paraentPath = dirs.join("/");
    return (
      <div style={{ padding: "20px" }}>
        <Container>
          {this.state.target_path}
          <Table>
            <Table.Header>
              <Table.HeaderCell>Cluster Names</Table.HeaderCell>
            </Table.Header>
            <Table.Body>
              {target_path == "/" ? (
                ""
              ) : (
                <Table.Row>
                  <Table.Cell>
                    <Link to={paraentPath}>..</Link>
                  </Table.Cell>
                </Table.Row>
              )}

              {clu_names.map((clu_name) => {
                return (
                  <Table.Row>
                    <Table.Cell>
                      <Link
                        to={
                          target_path == "/"
                            ? rootPath + clu_name
                            : rootPath + "/" + clu_name
                        }
                      >
                        {clu_name}
                      </Link>
                    </Table.Cell>
                  </Table.Row>
                );
              })}
            </Table.Body>
          </Table>
        </Container>
        <Header>Images ({totalImages})</Header>
        <GridGallery images={photos} />
        <PaginationExampleCustomization
          handlePaginationChange={this.handlePaginationChange}
          activePage={page}
          totalPages={totalPages}
        />
      </div>
    );
  }
}

export default Browser;
