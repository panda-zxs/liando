import * as echarts from 'echarts';
import Base from './BaseChart';
import china from './china.json';

import d from './test.geoJson';

const aa = require('./china.geoJson');

console.log('Json', china);
console.log('Json aa', aa);
console.log('geoJson', d);

// console.log(china);
echarts.registerMap('中国', china);

// @renderChart
export default class MapChart extends Base {
  public state = {
    routes: ['中国'],
  };

  public onChartDomClick = (e: React.SyntheticEvent) => {
    const { routes } = this.state;
    if (routes.length <= 1) return;
    this.setState(
      {
        routes: routes.slice(0, -1),
      },
      () => {
        this.myChart.setOption(this.getOption());
      },
    );
  };

  public chartEvents = {
    click: async (params: any) => {
      console.log('click', params);
      params.event.event.stopPropagation();
      // if (params.name === '河北') {
      const h = 'hebei';
      const res = await import(`./${h}.json`);
      console.log(res);
      echarts.registerMap('河北', res.default);
      this.setState(
        {
          routes: [...this.state.routes, '河北'],
        },
        () => {
          this.myChart.setOption(this.getOption());
        },
      );
      // }
    },
  };

  public getOption(): echarts.EChartOption {
    const { routes } = this.state;
    const ret: echarts.EChartOption = {
      tooltip: {
        trigger: 'item',
        formatter: '{b}',
      },
      geo: {
        map: routes[routes.length - 1],
        selectedMode: 'single',
        label: {
          emphasis: {
            show: false,
          },
        },
        itemStyle: {
          normal: {
            areaColor: '#004981',
            borderColor: '#064f85',
          },
          emphasis: {
            areaColor: '#1a5787',
          },
        },
      },
      series: [
        // {
        //   zlevel: 0,
        //   name: '中国',
        //   type: 'map',
        //   selectedMode: 'single',
        //   // @ts-ignore
        //   // mapType: 'china',
        // },
      ],
    };
    return ret;
  }
}
