import React from 'react';
import { Layout } from 'react-grid-layout';
import MapChart from '../../components/Chart/Map';
import GridLayout from '../../components/GridLayout';
import ScreenCard from '../../components/ScreenCard';
import style from './style.less';

const layout = [{ i: '.$map', x: 0, y: 0, w: 5, h: 6 }];

export default class Screen extends React.Component {
  public onChange = (layout: Layout[]) => {
    console.log(layout);
  };

  public render() {
    return (
      <div className={style.box}>
        <h1>Screen</h1>
        {/* <MapChart/> */}
        <GridLayout layout={layout} onLayoutChange={this.onChange}>
          <ScreenCard key="map">
            <MapChart />
          </ScreenCard>
        </GridLayout>
      </div>
    );
  }
}
